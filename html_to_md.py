from bs4 import BeautifulSoup

# Load HTML file
with open("certifications.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Output file
output_file = "README.md"

# Start Markdown output
with open(output_file, "w", encoding="utf-8") as md:
    # Banner
    banner = soup.find("img", {"alt": "Banner"})
    if banner:
        md.write(f'<img src="{banner["src"]}" width="{banner.get("width", "100%")}" height="{banner.get("height", "")}" alt="Banner"/>\n\n')

    for table in soup.find_all("table"):
        tds = table.find_all("td")

        if not tds:
            continue

        # Build 3 rows
        title_row = "|"
        separator_row = "|"
        badge_row = "|"
        issuer_row = "|"

        for td in tds:
            # Title
            title_tag = td.find("a", class_="cert-title")
            if title_tag:
                title = title_tag.get_text(strip=True)
                href = title_tag.get("href", "#")
                tooltip = title_tag.get("title", title)
                title_row += f' [*{title}*]({href} "{tooltip}") |'
            else:
                title_row += "  |"

            # Badge Image (first <img> tag)
            img_tags = td.find_all("img")
            badge_img_tag = img_tags[0] if len(img_tags) > 0 else None
            badge_link_tag = td.find("a", href=True)
            if badge_img_tag and badge_link_tag:
                badge_img = badge_img_tag.get("src", "")
                badge_width = badge_img_tag.get("width", "150")
                badge_link = badge_link_tag["href"]
                badge_title = badge_link_tag.get("title", title_tag.get_text(strip=True) if title_tag else "")
                badge_row += f' [<img src="{badge_img}" width="{badge_width}"/>]({badge_link} "{badge_title}") |'
            else:
                badge_row += "  |"

            # Issuer
            issuer_img_tag = img_tags[-1] if len(img_tags) > 0 else None
            issuer_link_tag = td.find_all("a")[-1] if td.find_all("a") else None
            if issuer_img_tag and issuer_link_tag:
                issuer_img = issuer_img_tag.get("src", "")
                issuer_width = issuer_img_tag.get("width", "70")
                issuer_link = issuer_link_tag.get("href", "#")
                issuer_alt = issuer_img_tag.get("alt", "Issuer")
                issuer_row += f' <i>Issued by</i><br>[<img src="{issuer_img}" width="{issuer_width}">]({issuer_link} "{issuer_alt}") |'
            else:
                issuer_row += "  |"

            separator_row += ":--:|"

        # Write rows to Markdown
        md.write(f"{title_row}\n{separator_row}\n{badge_row}\n{issuer_row}\n\n")

print("✅ certifications.md generated successfully.")