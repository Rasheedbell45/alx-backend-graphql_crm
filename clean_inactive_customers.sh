#!/bin/bash

DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lte=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $DELETED_COUNT inactive customers" >> /tmp/customercleanuplog.txt
