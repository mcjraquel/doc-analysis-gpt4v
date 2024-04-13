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
                        You are a Frappe/ERPNext developer who is an expert in creating Print Formats using Jinja. The image I will send next is a Sales Invoice, give me the
                        HTML mapping the fields in the image into their corresponding classes and HTML elements. The dimensions of the document should be 8.5 inches by 11 inches.
                        Do not include the label of the field, only the blank/space where the value should be written. Group the elements in the
                        document into different HTML class names, and specify the group where each field belongs. Here are the fields I need with their corresponding
                        field names, mapped as attributes of `doc` using Jinja:
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

                        The items in the table should be mapped as attributes of each `item` using Jinja, such that the following fields would fill in the blanks in the document. Also do the same thing for these:
                            1. Qty: qty
                            2. Unit of Measure: uom
                            3. Articles: item_name
                            4. Unit Price: rate
                            5. Amount: amount

                        For currency values, the value should be formatted using the `frappe.utils.fmt_money(value, currency=doc.currency)` function,
                        where value is the value of the field.

                        Additionally, give me the CSS code with the defined classes. The attributes of the classes of the fields should be specified in the CSS
                        in separate brackets, and should each have an undefined margin-left attribute. Make sure the classes of the sections also have separate class definitions and
                        should have a position attribute of "absolute" and undefined attributes of top, left, and width. The class pertaining to the
                        item details table should also have an undefined height, and a border-collapse attribute of "collapse". The class pertaining
                        to the item details table should also have a sub-group class for each row in the table, with a display attribute of "flex",
                        align-items attribute of "center", and an undefined height.

                        Only for the fields in each row in the table, follow these rules:
                            1. If the value in the field is a number, the text-align attribute should be "right", the overflow attribute should be "visible",
                            and the white-space attribute should be "nowrap".
                            2. If the value in the field is a text, the text-align attribute should be "left", the overflow attribute should be "hidden",
                            the white-space attribute should be "nowrap", and the text-overflow attribute should be "ellipsis".

                        Just give me the content of the body HTML tag and CSS separately, with no footnotes. Put `/* placeholder */` as placeholder text in the HTML where the values should be written, and
                        in the CSS where the undefined attributes are supposed to be defined.

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
