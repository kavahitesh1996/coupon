# Generated by Django 4.0.1 on 2022-01-09 07:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('code', models.CharField(help_text='Only uppercase letters & numbers are allowed.', max_length=32, validators=[django.core.validators.RegexValidator('^[A-Z0-9]*$', 'Only uppercase letters & numbers are allowed.')])),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=6)),
                ('start_date', models.DateTimeField()),
                ('expiration_date', models.DateTimeField()),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('flat', 'Flat')], max_length=32)),
                ('discount', models.PositiveIntegerField()),
                ('max_discount_amout', models.PositiveIntegerField(help_text='This is max amount users will get after the promo code is applied.')),
                ('number_of_uses', models.PositiveIntegerField(default=1, help_text='How many times this coupon will be used.')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CouponRedemption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order_amount', models.PositiveIntegerField()),
                ('actual_price', models.PositiveIntegerField(help_text='Order total amount after code redemption applied.')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promocode.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]