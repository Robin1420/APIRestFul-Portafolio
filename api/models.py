# models.py
# -*- coding: utf-8 -*-
from django.db import models


class Certificados(models.Model):
    titulo = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    institucion = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    enlace_certificado = models.CharField(max_length=300, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificados'


class DatosPersonales(models.Model):
    nombre = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    profesion = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    descripcion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # This field type is a guess.
    email = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    telefono = models.CharField(max_length=30, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    direccion = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    foto_perfil = models.BinaryField(blank=True, null=True)
    cv = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos_personales'


class Experiencias(models.Model):
    puesto = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    empresa = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    descripcion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # This field type is a guess.
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    actual = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiencias'


class Proyectos(models.Model):
    titulo = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    descripcion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # This field type is a guess.
    tecnologias = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)
    enlace_demo = models.CharField(max_length=300, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    enlace_codigo = models.CharField(max_length=300, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    visible = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyectos'


class RedesSociales(models.Model):
    plataforma = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    enlace = models.CharField(max_length=300, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    visible = models.BooleanField(blank=True, null=True)
    icono = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redes_sociales'


class Skills(models.Model):
    nombre = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    categoria = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'


class UsuariosAdmin(models.Model):
    username = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS')
    password_hash = models.CharField(max_length=300, db_collation='Modern_Spanish_CI_AS')
    email = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    creado_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios_admin'
