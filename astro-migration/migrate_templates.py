#!/usr/bin/env python3
"""
Script to migrate Django templates to Astro pages
Converts Django template syntax to Astro syntax
"""

import re
import os

def convert_django_to_astro(content, page_name):
    """Convert Django template to Astro format"""
    
    # Remove Django template tags
    content = re.sub(r'{%\s*extends\s+[\'"]base\.html[\'"]\s*%}', '', content)
    content = re.sub(r'{%\s*load\s+static\s*%}', '', content)
    content = re.sub(r'{%\s*block\s+title\s*%}.*?{%\s*endblock\s*%}', '', content, flags=re.DOTALL)
    content = re.sub(r'{%\s*block\s+extra_head\s*%}.*?{%\s*endblock\s*%}', '', content, flags=re.DOTALL)
    content = re.sub(r'{%\s*block\s+extra_css\s*%}.*?{%\s*endblock\s*%}', '', content, flags=re.DOTALL)
    content = re.sub(r'{%\s*block\s+content\s*%}', '', content)
    content = re.sub(r'{%\s*endblock\s*%}', '', content)
    
    # Convert URLs
    content = re.sub(r'{%\s*url\s+[\'"](\w+)[\'"]\s*%}', r'/\1', content)
    content = content.replace("{% url 'home' %}", "/")
    
    # Convert static files
    content = re.sub(r'{%\s*static\s+[\'"]([^\'\"]+)[\'"]\s*%}', r'/\1', content)
    
    # Remove Django comments
    content = re.sub(r'{#.*?#}', '', content, flags=re.DOTALL)
    
    # Convert Django variables to Astro (simple cases)
    content = re.sub(r'{{\s*(\w+)\s*}}', r'{\1}', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def create_astro_page(template_path, output_path, title):
    """Create Astro page from Django template"""
    
    print(f"Converting {template_path} -> {output_path}")
    
    # Read Django template
    with open(template_path, 'r', encoding='utf-8') as f:
        django_content = f.read()
    
    # Convert content
    astro_content = convert_django_to_astro(django_content, os.path.basename(template_path))
    
    # Create Astro file with frontmatter
    astro_file = f"""---
import Layout from '../layouts/Layout.astro';
---

<Layout title="{title}">
{astro_content}
</Layout>
"""
    
    # Write Astro file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(astro_file)
    
    print(f"✅ Created {output_path}")

# Main conversion
if __name__ == "__main__":
    base_django = "../templates/main"
    base_astro = "src/pages"
    
    pages = [
        ("resources.html", "resources.astro", "Resources - CodeVerseHub"),
        ("rules.html", "rules.astro", "Rules & Guidelines - CodeVerseHub"),
        ("faq.html", "faq.astro", "FAQ - CodeVerseHub"),
        ("about.html", "about.astro", "About - CodeVerseHub"),
    ]
    
    print("🚀 Starting Django to Astro migration...\n")
    
    for django_file, astro_file, title in pages:
        django_path = os.path.join(base_django, django_file)
        astro_path = os.path.join(base_astro, astro_file)
        
        if os.path.exists(django_path):
            create_astro_page(django_path, astro_path, title)
        else:
            print(f"⚠️  Django template not found: {django_path}")
    
    print("\n✅ Migration complete!")
    print("\nNext steps:")
    print("1. Review the generated Astro files")
    print("2. Test each page: npm run dev")
    print("3. Fix any remaining template syntax issues")
