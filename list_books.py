from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)
 
def list_books():
    resp = sb.table("books").select("*").order("book_id", desc=False).execute()
    return resp.data
 
if __name__ == "__main__":
    books = list_books()
    if books:
        print("books:")
        for p in books:
            print(f"{p['book_id']}: {p['title']} (author:{p['author']}) — category:{p['category']} — stock: {p['stock']}")
    else:
        print("No books found.")