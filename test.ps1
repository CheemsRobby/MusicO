from django.template.loader import get_template

try:
    template = get_template('player.html')
    print(f"Ä£°åÎ»ÖÃ£º{template.origin.name}")
except Exception as e:
    print(f"´íÎó£º{e}")