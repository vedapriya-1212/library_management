from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)
 
def search_book(id):
    resp = sb.table("books").select("*").eq("book_id",id).execute()
    return resp.data
 
if __name__ == "__main__":
    bid = int(input("Enter book_id to search: ").strip())
 
    search = search_book(bid)
    if search:
        print("book found:",search)
    else:
        print("No book found")