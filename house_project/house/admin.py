from django.contrib import admin
from .models import (UserProfile, Property, Region, City, District, HouseImage, LegalDocument, HouseReview,
                     Review, Favorite, Rental)
from modeltranslation.admin import TranslationAdmin

class RegionInline(admin.TabularInline):
    model = Region
    extra = 1

class CityInline(admin.TabularInline):
    model = City
    extra = 1

class DistrictInline(admin.TabularInline):
    model = District
    extra = 1

class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 1

class LegalDocumentInline(admin.TabularInline):
    model = LegalDocument
    extra = 1

@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    inlines = [RegionInline, CityInline, DistrictInline, HouseImageInline, LegalDocumentInline]


admin.site.register(UserProfile)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(District)
admin.site.register(HouseReview)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Rental)
