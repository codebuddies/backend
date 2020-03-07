from taggit.managers import _TaggableManager


class CustomTaggableManager(_TaggableManager):

    def guids(self):
        return self.get_queryset().values_list("guid", flat=True)

    def all_fields(self):
        return self.get_queryset().values()
