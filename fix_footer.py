import os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.html', '.css')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Remove footer borders or horizontal lines inside footer sections
            original = content
            content = content.replace('border-top', 'border-top: none !important;')
            content = content.replace('border-bottom', 'border-bottom: none !important;')
            
            if content != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Removed border in: {file}")
