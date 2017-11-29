__all__ = [
    'description',
    'maintainer',
    'maintainer_email',
    'url',
    'version_info',
    'version',
]

version_info = (0, 1)
version = '.'.join(map(bytes, version_info))

maintainer = 'Nick Joyce'
maintainer_email = 'nick.joyce@realkinetic.com'

description = """
Opinionated configuration library that uses a schema to validate before
allowing the app/service to continue serving.
""".strip()

url = 'https://github.com/RealKinetic/configur8'
