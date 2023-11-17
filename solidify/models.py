from django.db import models


# Create your models here.
class Endereco(models.Model):
    CEP = models.CharField(max_length=9)
    UF = models.CharField(max_length=2)
    CIDADE = models.CharField(max_length=255)
    BAIRRO = models.CharField(max_length=255)
    NUMERO = models.CharField(max_length=10)
    ENDERECO = models.CharField(max_length=255)

    class Meta:
        abstract = True


class ONG(Endereco):
    CNPJ = models.CharField(max_length=14, unique=True)
    NOME = models.CharField(max_length=255, null=False)
    SITUACAO = [(1, "ATIVO"), (2, "DESATIVADO"), ]
    STATUS = models.PositiveIntegerField(default=1, choices=SITUACAO, null=False)
    DATA_FUNDACAO = models.DateField(null=False)

    def __str__(self):
        return self.NOME

class Usuario(models.Model):
    NOME = models.CharField(max_length=255, null=False)
    EMAIL = models.EmailField(max_length=75, null=False)
    SENHA = models.CharField(max_length=255, null=False)
    CPF = models.CharField(max_length=15, null=False, unique=True)
    STATUS = models.BooleanField(default=True, null=False)


class Administrador(Usuario):
    ID_ONG = models.ForeignKey(ONG, on_delete=models.CASCADE)
    TP_PRIVILEGIOS = [("A", "ADMIN"), ("U", "USER")]
    PRIVILEGIO = models.CharField(default=True, choices=TP_PRIVILEGIOS, null=False)

class Voluntario(Usuario, Endereco):
    score = models.IntegerField(null=True)
