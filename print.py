import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                        You are a Frappe/ERPNext developer who is an expert in creating Print Formats. The image I will send after this is an
                        example of an image of a Sales Invoice template and the corresponding HTML and CSS that would render the document,
                        follow this as a template when building the HTML and CSS for the Sales Invoice Print Format:
                        ```html
                            {% from "bizkit_core/templates/print_formats/transaction_macros.html" import
                                set_transaction_values,
                                render_address
                            %}

                            {% set paginated_items = paginate_items(doc.items, 14) %}
                            {% for page_num in range(paginated_items|length) %}

                            <div class="receiptformat">
                                
                                <div class="top">
                                    <div style="margin-left: 1.25in; height: 0.358in; font-size: 150%;"></div>
                                    <div style="margin-left: 1.1in;">{{ doc.posting_date }}</div>
                                </div>
                                
                                <div class="small-box-1">
                                    <div style="margin-left: {{ 0.7 }}in;">{{ doc.customer }}</div>
                                    <div style="margin-left: {{ 0.7 * 0.5 }}in;">{{ doc.tax_id }}</div>
                                    <div style="margin-left: {{ 0.7 * 2 }}in; font-size: 80%;">{{ get_customer_address(doc.customer, True, {"is_primary_address": 1}) or "" }}</div>
                                </div>
                                
                                <div class="small-box-2">
                                    {% set ship_to = get_customer_address(doc.customer, True, {"is_shipping_address": 1}) %}
                                    <div style="margin-left: 0.5in;">
                                        {% if ship_to %}
                                            {{ ship_to }}
                                        {% else %}
                                            <br/>
                                            <br/>
                                            <br/>
                                        {% endif %}
                                    </div>
                                    <div style="height:0.257in;"></div>
                                    {% set contact = get_contact({"link_doctype": "Customer", "link_name": doc.customer}, {"is_primary_contact": 1}) %}
                                    <div style="margin-left: 0.5in; font-size: 80%;">
                                        {% if contact.mobile_no %}
                                            {{ contact.name }} ({{ contact.mobile_no }})
                                        {% else %}
                                            <br/>
                                        {% endif %}
                                    </div>
                                    
                                </div>
                                
                                <table class="items">
                                    {% for item in paginated_items[page_num] %}
                                        <tr class="item-row">
                                            <td class="item-qty">{{ item.qty }}</td>
                                            <td class="item-unit">{{ item.uom }}</td>
                                            <td class="item-description">{{ item.item_code }}: {{ item.item_name }}</td>
                                            <td class="item-price">{{ frappe.utils.fmt_money(item.rate, currency=doc.currency) }}</td>
                                            <td class="item-amount">{{ frappe.utils.fmt_money(item.amount, currency=doc.currency) }}</td>
                                        </tr>
                                    {% endfor %}
                                </table>
                                
                                <div class="sign">
                                    <span>
                                        <div class="text-center" style="background: white url('{{ frappe.db.get_value("User", doc.owner, "signature") }}') no-repeat;
                                            background-size: auto 70px;
                                            background-position: center;
                                            margin-left: 0.15in;
                                        ">
                                            <br />
                                            <br />
                                            <br />
                                            <br />
                                            <br />
                                        </div>
                                        <div>{{ frappe.db.get_value("User", doc.owner, "full_name") }}</div>
                                    </span>
                                    <span style="margin-left: 1.3in;">
                                        <div class="text-center" style="background: white url('{{ frappe.db.get_value("User", doc.approver, "signature") }}') no-repeat;
                                            background-size: auto 70px;
                                            background-position: center;
                                        ">
                                            <br />
                                            <br />
                                            <br />
                                            <br />
                                            <br />
                                        </div>
                                        <div>{{ frappe.db.get_value("User", doc.approver, "full_name") or "" }}</div>
                                    </span>
                                </div>
                                
                                <div class="totals">
                                    <p>{{ frappe.utils.fmt_money(doc.net_total, currency=doc.currency) }}</p>
                                    
                                    {% set vat_amounts = [] %}
                                    {% for tax in doc.taxes %}
                                        {% if frappe.db.get_value('Account', tax.account_head, 'account_name') == "Output VAT" %}
                                            {% if vat_amounts.append(tax.tax_amount) %}{% endif %}
                                        {% endif %}
                                    {% endfor %}
                                    <p>{{ frappe.utils.fmt_money((vat_amounts | sum), currency=doc.currency) }}</p>
                                    <p>{{ frappe.utils.fmt_money(doc.grand_total, currency=doc.currency) }}</p>
                                </div>
                            </div>
                            <!--{% if page_num + 1 != (paginated_items|length) %}-->
                            <!--    <div class="page-break"></div>-->
                            <!--{% endif %}-->
                            {% endfor %}
                        ```

                        ```css
                            .receiptformat {
                                font-family: "Lucida Console", "Courier New", monospace;
                                font-size: 14px;
                                position: relative;
                                left: 0px;
                                top: 0px;
                                width: 8.5in;
                                height: 11in;
                                page-break-before: always;
                            }

                            .top {
                                position: absolute;
                                left: 4.9in;
                                top: 0.9in;
                            }

                            .top > div {
                                height: 0.25in;
                            }

                            .small-box-1 {
                                position: absolute;
                                top: 2.125in;
                                left: 0.62in;
                                width: 3.5in;
                            }

                            .small-box-2 {
                                position: absolute;
                                top: 2.125in;
                                left: 4.9in;
                                width: 3.15in;
                            }

                            .items {
                                position: absolute;
                                top: 4.73in;
                                left: 0.585in;
                                width: 7.40in;
                                height: 3.95in;
                                border-collapse: collapse;
                                font-size: 90%;
                            }

                            .item-row {
                                display: flex;
                                height: 0.27in;
                                align-items: center;
                            }

                            .item-qty {
                                width: 0.9in;
                                text-align: right;
                                overflow-wrap: normal;
                                overflow: visible;
                                display: inline-block;
                                white-space: nowrap;
                            }

                            .item-unit {
                                width: 0.835in;
                                text-align: left;
                                overflow: hidden;
                                white-space: nowrap;
                                text-overflow: ellipsis;
                            }

                            .item-description {
                                width: 2.55in;
                                text-align: left;
                                overflow: hidden;
                                white-space: nowrap;
                                text-overflow: ellipsis;
                            }

                            .item-price {
                                width: 1.57in;
                                text-align: right;
                                overflow: visible;
                                white-space: nowrap;
                            }

                            .item-amount {
                                left: 5.6in;
                                width: 1.57in;
                                text-align: right;
                                overflow: visible;
                                display: inline-block;
                                white-space: nowrap;
                            }

                            .sign {
                                position: absolute;
                                top: 8.7in;
                                left: 0.585in;
                                width: 4.40in;
                                height: 1.3in;
                                font-size: 80%;
                                display: flex;
                            }

                            .sign > span {
                                width: 1.5in;
                            }

                            .sign > span > div {
                                width: inherit;
                                text-align: center;
                            }

                            .totals {
                                position: absolute;
                                top: 9.35in;
                                left: 6in;
                                width: 1.7in;
                                height: 1.5in;
                                font-size: 90%;
                            }

                            .totals > p {
                                text-align: right;
                            }
                        ```
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://t3850487.p.clickup-attachments.com/t3850487/d12a27df-0d34-4eaa-b4e9-0abf46a2acdf/image.png",
                        # "url": "https://drive.google.com/file/d/1GIxFRwMv_xMjdaKz2umG8wMMT0crJ5Op/view?usp=sharing",
                        "detail": "high",
                    },
                },
                {
                    "type": "text",
                    "text": """
                        The image I will send next is a Sales Invoice, give me the HTML with Jinja mapping
                        and CSS that will render the document in the image with the exact same format, dimensions and alignments per field. Its dimensions should be 8.5 inches by 11 inches.
                        The margins should be specified in inches in the HTML and CSS such that all fields in the HTML are aligned with their corresponding
                        blank or space in the document given. Group the elements in the document into different div tags. The values in the HTML should be mapped
                        as attributes of `doc` such that the following fields would fill in their corresponding blanks in the document:
                            1. Sold To: customer_name
                            2. Address: address_display
                            3. Date: posting_date
                            4. Terms: payment_terms_template
                            5. P.O. No.: po_no
                            6. P.R. No.: (set to "None")
                            7. TIN: tax_id
                            8. Item Details: items
                            9. Tax Details: taxes_and_charges
                            10. Total Amount Due: grand_total
                            11. Deliver To: shipping_address
                            12. To: contact_display
                            13. Total Sales (VAT Inclusive): net_total
                            13. Less VAT: (computed from the `taxes` table, getting the total of the amount column of rows wherein the account name is "Input VAT")
                            14. Business Style: customer_name
                            15. Amount Net of VAT: (computed by subtracting the VAT from the Total Sales)
                            16. Add VAT: (computed from the `taxes` table, getting the total of the amount column of rows wherein the account name is "Output VAT")

                        The items should be mapped such that the following fields would fill in the blanks in the document:
                            1. Qty: qty
                            2. Unit: uom
                            3. Articles: item_name
                            4. Unit Price: rate
                            5. Amount: amount

                        The alignments should work when the values on the HTML are overlain on the document.
                        Just give me the HTML and CSS separately with no other text and notes.
                        Make sure the HTML and CSS would render the document exactly the same as the image.
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://drive.usercontent.google.com/download?id=1bBqbGvPWQEP52cI-2ne55X8CcNT0IvZf&authuser=1",
                        "detail": "high",
                    },
                },
            ],
        }
    ],
    # max_tokens=500,
    max_tokens=4096,
)
print(response.choices[0].message.content)
