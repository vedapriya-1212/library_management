#delete member if no book borrowed
from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def delete_member(member_id: int):
    # 1. Check if the member has unreturned books
    borrowed = sb.table("borrow_records").select("*").eq("member_id", member_id).is_("return_date", None).execute()
    

    if borrowed.data:  # If any active borrowings exist
        print(f"Member {member_id} cannot be deleted — they still have borrowed books.")
        return None

    # 2. If no active borrowings, delete the member
    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    return resp.data

if __name__ == "__main__":
    mid = int(input("Enter member_id to delete: ").strip())
    confirm = input(f"Are you sure you want to delete member {mid}? (yes/no): ").strip().lower()

    if confirm == "yes":
        deleted = delete_member(mid)
        if deleted:
            print("Deleted:", deleted)
        else:
            print("No member deleted (check member_id or borrowing records).")
    else:
        print("Delete cancelled.")
