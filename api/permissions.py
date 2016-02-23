from rest_framework import permissions

class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
	"""Permission class that controls access to a certain view"""
	def has_permission(self, request, view):
		"""Method the chects whether the request has necessary permisiions"""
		if request.method == 'POST':
		    return True
		return super(IsAuthenticatedOrCreate, self).has_permission(request, view)