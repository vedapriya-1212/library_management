import os
from supabase import create_client, Client #pip install supabase
from dotenv import load_dotenv # pip install python-dotenv
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)
 
def add_borrow(mid,bid):
    borrow = {"member_id": mid,"book_id": bid}
    resp = sb.table("borrow_records").insert(borrow).execute()
    return resp.data
 
if __name__ == "__main__":
    mid = input("Enter member_id: ").strip()
    bid = input("Enter book_id: ").strip()
    created = add_borrow(mid, bid)
    print("Inserted:", created)