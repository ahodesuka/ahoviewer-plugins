import gi
import json
import re
gi.require_version('Ahoviewer', '1.0')
from gi.repository import Ahoviewer, GLib, GObject

class PythonHelloPlugin(GObject.Object, Ahoviewer.SiteActivatable):

  tag_type_map = {
    0 : Ahoviewer.TagType.GENERAL,
    1 : Ahoviewer.TagType.ARTIST,
    2 : Ahoviewer.TagType.COPYRIGHT,
    3 : Ahoviewer.TagType.COPYRIGHT,
    4 : Ahoviewer.TagType.CHARACTER,
    5 : Ahoviewer.TagType.GENERAL,
    8 : Ahoviewer.TagType.METADATA,
  }

  def __init__(self):
    GObject.Object.__init__(self)

  def _get_booru_url(self, url):
    # This doesn't exist
    #if "iapi." in url:
    #  return "https://idol.sankakucomplex.com"
    return "https://chan.sankakucomplex.com"

  def do_get_test_uri(self):
    return "/posts?page=1&limit=1"

  def do_get_posts_uri(self, tags, page, limit):
    return f"/posts?lang=english&page={page}&limit={limit}&tags={tags}"

  # Authentication not supported
  # Doesn't need to be implemented, if its not supported
  #def do_get_register_url(self, url):
  #  pass

  # The API and the actual booru have different subdomains
  # Can either be a direct url to a valid image, or a url where favicon.{ico,png} exists
  # Doesn't need to be implemented, if the favicon.{ico,png} exists on the api url
  def do_get_icon_url(self, url):
    return self._get_booru_url(url) + "/favicon.png"

  # _ = data size, not needed here but I can't find a way to prevent libpeas from sending it
  def do_parse_post_data(self, data, _, url, samples):
    posts = []
    notes_url = url + "/posts/{id}/notes"

    for post in json.loads(data):
      tags = []
      for tag in post["tags"]:
        if tag["name"] == None:
          continue
        try:
          tt = self.tag_type_map[tag["type"]]
        except KeyError:
          tt = Ahoviewer.TagType.UNKNOWN
        tags.append(Ahoviewer.Tag.new(tag["name"], tt))

      p = Ahoviewer.Post.new(tags)
      p.image_url = post["sample_url"] if samples else post["file_url"]
      p.thumb_url = post["preview_url"]
      p.post_url  = self._get_booru_url(url) + "/post/show/{}".format(post["id"])
      p.notes_url = notes_url.format(id=post["id"]) if post["has_notes"] else ""

      # This is a unix timestamp, ahoviewer will take care of converting it to
      # a formatted date string
      p.date   = post["created_at"]["s"]
      p.source = post["source"]
      p.rating = post["rating"]
      p.score  = str(post["total_score"])

      posts.append(p)

    # Sankaku doesn't have a counts API or give total posts here
    # and doesn't have any error messages to parse as far as I have seen
    return Ahoviewer.Posts.new(posts, 0, "")

  def do_parse_note_data(self, data, _):
    notes = []
    for note in json.loads(data):
      if not note["is_active"]:
        continue

      body = re.sub("<[^>]*>", "", note["body"])
      notes.append(Ahoviewer.Note.new(body, note["width"], note["height"], note["x"], note["y"]))

    return notes
