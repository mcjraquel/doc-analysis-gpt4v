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
                    "text": """If the document in the image is a Sales Invoice, give me a JSON containing the following information, substituting the labels with the corresponding keys below:
                        1. Customer: customer
                        2. Customer's Address: customer_address
                        3. Invoice Date: posting_date
                        4. Payment Terms: payment_terms_template
                        5. Purchase Order (PO) No.: purchase_order
                        6. Purchase Receipt (PR) No.: purchase_receipt
                        7. TIN: tax_id
                        8. Item Details: items
                        9. Tax Details: taxes_and_charges
                        10. Total Amount Due: grand_total
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": "https://media.discordapp.net/attachments/1022675473156812882/1171345066560847903/6a0b0f88-19e6-46b7-8300-1240054441c2.png?ex=6578069a&is=6565919a&hm=0313238c19e0d88672a8062a26d3f84ae56d3ec08670518bbb18a061d46e9ef2&=&format=webp&quality=lossless&width=750&height=1002",
                },
            ],
        }
    ],
    # max_tokens=500,
    max_tokens=4096,
)
print(response.choices[0].message.content)
