# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'paypalx_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('currency', self.gf('django.db.models.fields.TextField')(max_length=50)),
            ('token', self.gf('django.db.models.fields.CharField')(null=True, default=None, max_length=250, blank=True, unique=True, db_index=True)),
            ('payer_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_after_set', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('date_paid', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('buyer_email', self.gf('django.db.models.fields.EmailField')(default=None, max_length=75, null=True, blank=True)),
            ('buyer_country', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('buyer_first_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('buyer_last_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('set_ec_correlation_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('do_ec_correlation_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'paypalx', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table(u'paypalx_transaction')


    models = {
        u'paypalx.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'buyer_country': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'buyer_email': ('django.db.models.fields.EmailField', [], {'default': 'None', 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'buyer_first_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'buyer_last_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'currency': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'date_after_set': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_paid': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'do_ec_correlation_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payer_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'set_ec_correlation_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': 'None', 'max_length': '250', 'blank': 'True', 'unique': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['paypalx']