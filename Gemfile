source 'https://rubygems.org'

require 'json'
require 'open-uri'
versions = JSON.parse(open('https://pages.github.com/versions.json', :proxy=>'http://proxy.is.depaul.edu:3128').read)

gem "jekyll", "~> 3.9.0"
gem 'bigdecimal'
gem 'github-pages', 223 #versions['github-pages']
gem 'jekyll-compose', group: [:jekyll_plugins]
