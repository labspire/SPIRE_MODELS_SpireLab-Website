import os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.html', '.css')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            updated = False
            if '<hr' in content:
                content = content.replace('<hr', '<!-- <hr').replace('>', '-->')
                updated = True
            
            if updated:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Cleaned line in: {file}")
