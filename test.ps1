from django.template.loader import get_template

try:
    template = get_template('player.html')
    print(f"ģ��λ�ã�{template.origin.name}")
except Exception as e:
    print(f"����{e}")