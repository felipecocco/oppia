# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers for Oppia resources (templates, images)."""

__author__ = 'sll@google.com (Sean Lip)'

import json
from controllers.base import BaseHandler
import feconf
from models.models import Image
import utils


class LibHandler(BaseHandler):
    """Assembles and returns CSS and JS library code."""

    # The CSS and JS code to include in the header of each response.
    CSS_LIB_CODE = '\n'.join([
        utils.get_file_contents('', filepath)
        for filepath in feconf.ALL_CSS_LIBS])

    JS_LIB_CODE = '\n'.join([
        utils.get_file_contents(feconf.THIRD_PARTY_DIR, filepath)
        for filepath in feconf.THIRD_PARTY_JS_LIBS])

    def get(self, lib_type):
        """Handles GET requests for CSS and JS library code."""
        if lib_type == 'css':
            self.response.out.write(self.CSS_LIB_CODE)
            self.response.headers['Content-Type'] = 'text/css'
        elif lib_type == 'js':
            self.response.out.write(self.JS_LIB_CODE)
            self.response.headers['Content-Type'] = 'application/javascript'
        else:
            self.error(404)


class TemplateHandler(BaseHandler):
    """Retrieves an editor template."""

    def get(self, template_type):
        """Handles GET requests."""
        self.response.out.write(feconf.JINJA_ENV.get_template(
            'editor/views/%s_editor.html' % template_type).render({}))


class ImageHandler(BaseHandler):
    """Handles image uploads and retrievals."""

    def get(self, image_id):
        """Returns an image.

        Args:
            image_id: string representing the image id.
        """
        image = utils.get_entity(Image, image_id)
        if image:
            # TODO(sll): Support other image types.
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(image.image)
        else:
            self.response.out.write('No image')

    def post(self):
        """Saves an image uploaded by a content creator."""
        # TODO(sll): Check that the image is really an image.
        image = self.request.get('image')
        if image:
            image_hash_id = utils.get_new_id(Image, image)
            image_entity = Image(hash_id=image_hash_id, image=image)
            image_entity.put()
            self.response.out.write(json.dumps(
                {'image_id': image_entity.hash_id}))
        else:
            raise self.InvalidInputException('No image supplied')
            return