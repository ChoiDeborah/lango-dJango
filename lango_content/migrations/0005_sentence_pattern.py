# Generated by Django 2.1.4 on 2019-01-16 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lango_content', '0004_auto_20190116_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='pattern',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pattern_tag', to='lango_content.Pattern'),
            preserve_default=False,
        ),
    ]
