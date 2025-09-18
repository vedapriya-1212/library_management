from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def get_members_with_books():
    
    members = sb.table("members").select("*").execute().data
    
    borrow_records = (
        sb.table("borrow_records")
        .select("record_id, member_id, borrow_date, return_date, books(title, author, book_id)")
        .execute()
        .data
    )
    
    # Merge in Python
    member_map = {m["member_id"]: m for m in members}
    for m in member_map.values():
        m["borrowed_books"] = []
    
    for br in borrow_records:
        member_id = br["member_id"]
        if member_id in member_map:
            member_map[member_id]["borrowed_books"].append({
                "book_id": br["books"]["book_id"],
                "title": br["books"]["title"],
                "author": br["books"]["author"],
                "borrow_date": br["borrow_date"],
                "return_date": br["return_date"],
            })
    
    return list(member_map.values())


if __name__ == "__main__":
    data = get_members_with_books()
    for m in data:
        print(f"\nMember: {m['name']} ({m['email']})")
        if m["borrowed_books"]:
            for b in m["borrowed_books"]:
                print(f"  - {b['title']} by {b['author']} (Borrowed: {b['borrow_date']}, Returned: {b['return_date']})")
        else:
            print("  No books borrowed")