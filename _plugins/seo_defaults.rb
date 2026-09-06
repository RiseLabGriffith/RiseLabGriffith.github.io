# frozen_string_literal: true

# Project pages describe themselves with `summary` (shown on cards and under the heading). Reuse it as the
# meta description that jekyll-seo-tag emits, unless a project sets `description` explicitly.
# Runs once all files are read, so front matter is available.
Jekyll::Hooks.register :site, :post_read do |site|
  projects = site.collections["projects"]
  next unless projects

  projects.docs.each do |doc|
    doc.data["description"] ||= doc.data["summary"]
  end
end
