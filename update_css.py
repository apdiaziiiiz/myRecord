# import re

# with open('journal/static/journal/css/style.css', 'r') as f:
#     content = f.read()

# # Roots
# content = content.replace(''':root {
#     --bg-color: #0a0a0a;
#     --card-bg: #1a1a1a;
#     --primary-color: #ff6b00;
#     --primary-hover: #e66000;
#     --text-color: #f5f5f5;
#     --text-dim: #a0a0a0;
#     --border-color: #333;
#     --accent-orange: #ff8533;
#     --glass-bg: rgba(255, 255, 255, 0.05);
#     --glass-border: rgba(255, 255, 255, 0.1);''', ''':root {
#     /* New Palette */
#     --palette-mint: #B4DED1;
#     --palette-grey: #E2EAE1;
#     --palette-cream: #F7F6F0;
#     --palette-rose: #D99B9B;
#     --palette-dark: #333;

#     --bg-color: var(--palette-cream);
#     --card-bg: #FFFFFF;
#     --primary-color: var(--palette-rose);
#     --primary-hover: #c48787;
#     --text-color: var(--palette-dark);
#     --text-dim: #718096;
#     --border-color: var(--palette-grey);
#     --accent-orange: var(--palette-rose);
#     --glass-bg: rgba(255, 255, 255, 0.8);
#     --glass-border: rgba(0, 0, 0, 0.05);''')

# content = content.replace('''    /* New Palette */
#     --palette-mint: #B4DED1;
#     --palette-grey: #E2EAE1;
#     --palette-cream: #F7F6F0;
#     --palette-rose: #D99B9B;
#     --palette-dark: #333;
# }''', '''}''')

# # Sidebar
# content = content.replace('''    background-color: #000;
#     border-right: 1px solid var(--border-color);
#     padding: 2rem 1.5rem;''', '''    background-color: var(--palette-grey);
#     border-right: 1px solid var(--border-color);
#     padding: 2rem 1.5rem;''')

# # Logo span
# content = content.replace('''.logo span {
#     color: #fff;
# }''', '''.logo span {
#     color: var(--palette-dark);
# }''')

# # btn-primary
# content = content.replace('''.btn-primary {
#     background-color: var(--primary-color);
#     color: #000;
# }

# .btn-primary:hover {
#     background-color: var(--primary-hover);
#     transform: translateY(-2px);
#     box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3);
# }''', '''.btn-primary {
#     background-color: var(--primary-color);
#     color: #fff;
# }

# .btn-primary:hover {
#     background-color: var(--primary-hover);
#     transform: translateY(-2px);
#     box-shadow: 0 4px 15px rgba(217, 155, 155, 0.3);
# }''')

# # card
# content = content.replace('''.card {
#     background-color: var(--card-bg);
#     border: 1px solid var(--border-color);
#     border-radius: 20px;
#     padding: 1.5rem;
#     position: relative;
#     overflow: hidden;
# }''', '''.card {
#     background-color: var(--card-bg);
#     border: 1px solid var(--border-color);
#     border-radius: 20px;
#     padding: 1.5rem;
#     position: relative;
#     overflow: hidden;
#     box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
# }''')

# # calendar day
# content = content.replace('''.calendar-day:hover {
#     background-color: #252525;
#     transform: scale(1.02);
# }''', '''.calendar-day:hover {
#     background-color: var(--palette-cream);
#     transform: scale(1.02);
#     box-shadow: 0 5px 15px rgba(0,0,0,0.05);
# }''')

# # Form
# content = content.replace('''.form-label {
#     display: block;
#     margin-bottom: 1rem;
#     font-weight: 800;
#     color: #fff;''', '''.form-label {
#     display: block;
#     margin-bottom: 1rem;
#     font-weight: 800;
#     color: var(--palette-dark);''')

# content = content.replace('''.form-control {
#     width: 100%;
#     background-color: #111;
#     border: 1px solid var(--border-color);
#     border-radius: 16px;
#     padding: 1.2rem;
#     color: #fff;
#     font-size: 1.1rem;
#     transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
# }''', '''.form-control {
#     width: 100%;
#     background-color: var(--card-bg);
#     border: 1px solid var(--border-color);
#     border-radius: 16px;
#     padding: 1.2rem;
#     color: var(--text-color);
#     font-size: 1.1rem;
#     transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#     box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
# }''')

# content = content.replace('''.form-control:focus {
#     outline: none;
#     border-color: var(--primary-color);
#     background-color: #161616;
#     box-shadow: 0 0 0 4px rgba(255, 107, 0, 0.1);
# }''', '''.form-control:focus {
#     outline: none;
#     border-color: var(--primary-color);
#     background-color: #fff;
#     box-shadow: 0 0 0 4px rgba(217, 155, 155, 0.2);
# }''')

# content = content.replace('''.mood-box {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     padding: 10px;
#     background-color: #111;
#     border: 2px solid transparent;
#     border-radius: 20px;
#     cursor: pointer;
#     transition: all 0.3s ease;
#     width: 114px;
#     height: 130px;
# }''', '''.mood-box {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     padding: 10px;
#     background-color: var(--card-bg);
#     border: 2px solid var(--border-color);
#     border-radius: 20px;
#     cursor: pointer;
#     transition: all 0.3s ease;
#     width: 114px;
#     height: 130px;
#     box-shadow: 0 4px 15px rgba(0,0,0,0.02);
# }''')

# content = content.replace('''.mood-box:hover {
#     background-color: #1a1a1a;
#     transform: translateY(-5px);
# }''', '''.mood-box:hover {
#     background-color: var(--palette-cream);
#     transform: translateY(-5px);
#     box-shadow: 0 10px 25px rgba(0,0,0,0.08);
# }''')

# content = content.replace('''.mood-option input:checked + .mood-box {
#     border-color: var(--primary-color);
#     background-color: rgba(255, 107, 0, 0.1);
#     box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
# }''', '''.mood-option input:checked + .mood-box {
#     border-color: var(--primary-color);
#     background-color: rgba(217, 155, 155, 0.1);
#     box-shadow: 0 10px 20px rgba(217, 155, 155, 0.2);
# }''')

# content = content.replace('''.media-pill {
#     display: inline-flex;
#     align-items: center;
#     gap: 0.6rem;
#     padding: 0.5rem 1.2rem;
#     background: #0d1117;
#     border: 1px solid #21262d;
#     border-radius: 50px;
#     cursor: pointer;
#     font-size: 0.9rem;
#     font-weight: 600;
#     color: var(--primary-color);
#     transition: all 0.3s ease;
# }''', '''.media-pill {
#     display: inline-flex;
#     align-items: center;
#     gap: 0.6rem;
#     padding: 0.5rem 1.2rem;
#     background: #fff;
#     border: 1px solid var(--border-color);
#     border-radius: 50px;
#     cursor: pointer;
#     font-size: 0.9rem;
#     font-weight: 600;
#     color: var(--primary-color);
#     transition: all 0.3s ease;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.05);
# }''')

# content = content.replace('''.media-pill:hover {
#     border-color: var(--primary-color);
#     background: #161b22;
#     transform: translateY(-2px);
#     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
# }''', '''.media-pill:hover {
#     border-color: var(--primary-color);
#     background: var(--palette-cream);
#     transform: translateY(-2px);
#     box-shadow: 0 4px 12px rgba(217, 155, 155, 0.2);
# }''')

# content = content.replace('''.media-pill i {
#     font-size: 0.9rem;
#     color: #fff;
# }''', '''.media-pill i {
#     font-size: 0.9rem;
#     color: var(--palette-dark);
# }''')

# content = content.replace('''background: rgba(255, 107, 0, 0.1);
#     border: 1px solid rgba(255, 107, 0, 0.2);''', '''background: rgba(217, 155, 155, 0.1);
#     border: 1px solid rgba(217, 155, 155, 0.2);''')

# with open('journal/static/journal/css/style.css', 'w') as f:
#     f.write(content)
# print("Updated style.css")
