import os
import markdown

def build_site():
    with open("templates/post_layout.html", "r", encoding="utf-8") as f:
        template = f.read()

    os.makedirs("docs/posts", exist_ok=True)

    posts_meta = []

    for filename in os.listdir("posts"):
        if filename.endswith(".md"):
            with open(f"posts/{filename}", "r", encoding="utf-8") as f:
                lines = f.readlines()

            title = lines[0].replace("title:", "").strip()
            date = lines[1].replace("date:", "").strip()

            body_text = "".join(lines[2:])
            html_content = markdown.markdown(body_text)

            final_html = template.replace("{{ title }}", title).replace("{{ content }}", html_content)

            output_filename = filename.replace(".md", ".html")
            with open(f"docs/posts/{output_filename}", f"w", encoding="utf-8") as f:
                f.write(final_html)

            posts_meta.append({"title": title, "date": date, "url": f"posts/{output_filename}"})
            print(f"Compiled: {output_filename}")
        
    build_index(posts_meta)

def build_index(posts):
    # Quick index builder to link your posts on the homepage
    links = "".join([f"<li>{p['date']} - <a href='{p['url']}'>{p['title']}</a></li>" for p in posts])
    index_html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>My Journal</title></head>
    <body style="font-family:sans-serif; max-width:600px; margin:40px auto; padding:0 20px;">
        <h1>My Personal Journal</h1>
        <ul>{links}</ul>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Homepage index updated!")

if __name__ == "__main__":
    build_site()