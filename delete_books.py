#delete member if no book borrowed
from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def delete_books(book_id: int):
     # Step 1: Check if book is currently borrowed (return_date is NULL)
    borrowed = (
        sb.table("borrow_records").select("*").eq("book_id", book_id).is_("return_date", None).execute()
    )

    if borrowed.data:  # If list not empty → book is borrowed
        return {"error" : "Book is currently borrowed. Cannot delete."}

    # Step 2: Delete the book since it’s not borrowed
    deleted = sb.table("books").delete().eq("book_id", book_id).execute()
    return deleted.data


if __name__ == "__main__":
    bid = int(input("Enter book_id to delete: ").strip())
    confirm = input(f"Are you sure you want to delete book {bid}? (yes/no): ").strip().lower()
    if confirm == "yes":
        result = delete_books(bid)
        if isinstance(result, dict) and "error" in result:
            print(result["error"])
        elif result:
            print("Deleted:", result)
        else:
            print("No book deleted — check book_id.")
    else:
        print("Delete cancelled.")