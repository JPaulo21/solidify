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
    CNPJ = models.CharField(max_length=18, unique=True)
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
    TP_USUARIO = [("A", "ADMIN"), ("V", "VOLUNTARIO")]
    TIPO = models.CharField(choices=TP_USUARIO, null=False)

class Administrador(Usuario):
    ID_ONG = models.ForeignKey(ONG, on_delete=models.CASCADE)
    TP_PRIVILEGIOS = [("A", "ADMIN"), ("U", "USER")]
    PRIVILEGIO = models.CharField(choices=TP_PRIVILEGIOS, null=False)

class Voluntario(Usuario, Endereco):
    SCORE = models.IntegerField(null=True)
    DATA_NASC = models.DateField(null=False)

class Evento(Endereco):
    ID_ONG = models.ForeignKey(ONG, on_delete=models.CASCADE)
    ONG_NOME = models.CharField(max_length=255, null=False)
    ID_ADMINISTRADOR = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    TITULO = models.CharField(max_length=255, null=False)
    DESCRICAO = models.CharField(max_length=1000, null=False)
    DATA_REALIZACAO = models.DateField(null=False)
    STATUS = models.BooleanField(default=True, null=False)
    NR_VOLUNTARIOS = models.IntegerField(null=False)
    NR_OCUPADOS = models.IntegerField(null=False, default=0)
    DATA_CANCELAMENTO = models.DateField(null=True)
    MOTIVO_CANCELAMENTO = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'id:{self.pk}, titulo {self.TITULO}, ONG: {self.ID_ONG}'

class Voluntarios_Evento(models.Model):
    ID_ONG = models.ForeignKey(ONG, on_delete=models.CASCADE)
    ID_EVENTO = models.ForeignKey(Evento, on_delete=models.CASCADE)
    ID_VOLUNTARIO = models.ForeignKey(Voluntario, on_delete=models.CASCADE, null=True)
    CPF_VOLUNTARIO = models.CharField(max_length=15, null=True)
    NOME = models.CharField(max_length=255, null=True)
    CARGO = models.CharField(max_length=60, null=False)

    def __str__(self):
        return f'id:{self.pk}, id_evento {self.ID_EVENTO}, cargo: {self.CARGO}, id_voluntário: {self.ID_VOLUNTARIO} \n'

    class Meta:
        unique_together = [['ID_EVENTO','ID_VOLUNTARIO']]
