#!/bin/bash

# Absolute path to your Django project
PROJECT_DIR="/path/to/alx-backend-graphqlcrm"
MANAGE="$PROJECT_DIR/manage.py"
LOGFILE="/tmp/customercleanuplog.txt"

# Change into the project directory so manage.py runs correctly
cd $PROJECT_DIR || exit 1

# Run the Django cleanup using manage.py shell
DELETED_COUNT=$(python "$MANAGE" shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lte=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")

# Log the result with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$DELETED_COUNT inactive customers\" >> \"$LOGFILE\"
