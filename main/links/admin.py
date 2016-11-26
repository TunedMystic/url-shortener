from django.contrib import admin

from .models import Link, Tag


class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_addresses',)

    def unique_addresses(self, instance):

        unique_ips = instance.addresses.count()
        if unique_ips >= 50:
            return '{} Unique IP Addresses'.format(unique_ips)

        return '\n'.join(address.address for address in instance.addresses.all())

# Register your models here.
admin.site.register(Link, LinkAdmin)
admin.site.register(Tag)
