from django.contrib import admin
from kb.models import Language, Snippet
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

class SnippetAdmin(admin.ModelAdmin):
    exclude             = ('author', 'slug')
    date_hierarchy      = 'date_created'
    ordering            = ('-date_created',)
    list_display        = ('title', 'language', 'view_on_site')
    list_filter         = ('language',)
    search_fields       = ('title', 'description', 'code')

    def view_on_site(self, obj):
        string = '<a href="%s">View on site &raquo;</a>' % (obj.get_absolute_url(),)
        return mark_safe(string)
    view_on_site.allow_tags = True
    view_on_site.short_description = 'Link'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
            obj.slug   = slugify(obj.title)
        obj.save()

admin.site.register(Snippet, SnippetAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'mime_type')

admin.site.register(Language, LanguageAdmin)