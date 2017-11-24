from django import template

register = template.Library()


@register.filter(name='has_tune_favori')
def has_tune_favori(self, user):
    if user.tunes_favoris.filter(of_tune__slug=self.slug).exists():
        return True
    else:
        return False


@register.filter(name='group_has_tune_favori')
def group_has_tune_favori(self, tune):
    if self.tunes_favoris.filter(of_tune__slug=tune.slug).exists():
        return True
    else:
        return False

