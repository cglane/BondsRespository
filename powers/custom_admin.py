from django.contrib.admin import AdminSite
from django.conf import settings
from django.views.decorators.cache import never_cache

from powers.template_helper import convert_type, agent_powers_count


power_type_headers = ["PK{}".format(convert_type(x)) for x in settings.POWERS_TYPES]


class CustomAdminSite(AdminSite):
	# set values for `site_header`, `site_title`, `index_title` etc.
	# extend / override admin views, such as `index()`
	@never_cache
	def index(self, request, extra_context=None):
		print('here')
		extra_context = extra_context or {}

		# do whatever you want to do and save the values in `extra_context`
		extra_context = {
			'all_agents': agent_powers_count(),
			'power_type_headers': power_type_headers,
			'power_types': [x[0] for x in settings.POWERS_TYPES]
		}
		return super(CustomAdminSite, self).index(request, extra_context)


custom_admin_site = CustomAdminSite()