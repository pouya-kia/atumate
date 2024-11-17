from django.db import models

# Create your models here.
STEP_DOC = (
    (0,'step1'),
    (1, 'step2'),
    (2, 'step3'),
)


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    last_modeified = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class DataLog(BaseModel):
    ...
    # data_json = copy last data
    # change option (what change?)
    # comment (TextField) description
    # step intfield (choose=STEP_DOC)
    # data_unique_code 
    # customer 

class Files(BaseModel):
    # COMMET: customer foriegnkey to user model
    file = models.URLField(verbose_name="files", max_length=200)
    file_status = models.BooleanField(verbose_name="file status", default=True)


    def __str__(self):
        return str(self.file) + " " + str(self.file_status)
    
class Dataset(BaseModel):
    # COMMENT: customer foriegnkey to user model
    parent_file = models.ForeignKey(Files, verbose_name="parent file", on_delete=models.CASCADE)
    data_unique_code = models.IntegerField(verbose_name="unique code for dataset")
    data_json = models.JSONField(verbose_name="data json")
    dataset_status = models.BooleanField(verbose_name="dataset status", default=True)

    def __str__(self):
        return str(self.data_unique_code) + "," + str(self.parent_file)

# COMMNET: file
# COMMENT: data_unique_code generated
# COMMENT: create = Dataset.objects.create(parent_file=file, data_json=data_json, data_unique_code=data_unique_code)
# request user , session user
