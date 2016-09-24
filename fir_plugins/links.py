from django.core.urlresolvers import reverse
import re


class Links(object):
    def __init__(self):
        self.reverse_links = []
        self.regex_links = []

    def register_reverse_link(self, parser_regex, url_name):
        """
        Registers a new parser for links using Django urlconf
        :param parser_regex: string or regex object
        :param url_name: urlconf name
        """
        if not isinstance(parser_regex, re._pattern_type):
            parser_regex = re.compile(parser_regex)
        self.reverse_links.append((parser_regex, url_name))

    def register_regex_link(self, parser_regex, template):
        """
        Registers a new parser for links using regex replacement
        :param parser_regex: string or regex object
        :param template: template to pass to regex expand
        """
        if not isinstance(parser_regex, re._pattern_type):
            parser_regex = re.compile(parser_regex)
        self.regex_links.append((parser_regex, template))

    def _reverse(self, request=None):
        patterns = []
        for regex, url in self.reverse_links:
            def get_url(match):
                path = reverse(url, args=match.groups())
                if request is not None:
                    return request.build_absolute_uri(path)
                return path
            patterns.append((regex, get_url))
        return patterns

    def link_patterns(self, request=None):
        links = list(self.regex_links)
        links.extend(self._reverse(request=request))
        return links

registry = Links()
