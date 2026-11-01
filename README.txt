WEIMAR FAMILY — GITHUB PAGES EDITION

The website is in docs/. It is plain HTML, local graphics and original photos.
No installation, build step, database or WordPress is needed.

PUBLISH A PREVIEW ON GITHUB

1. Create a repository named weimar-family-history (or another name you prefer).
   Use a public repository for GitHub Free, or a private repository if your plan
   supports GitHub Pages from private repositories.
2. Add this folder's CONTENTS to the repository using Git or GitHub Desktop.
   Keep docs/, tools/, reports/, templates/ and this README at the repository root.
   Commit the individual files, not the ZIP download: the ZIP is only a package.
3. In repository Settings > Pages, choose "Deploy from a branch", select main,
   choose /docs, and Save. If you use a different branch, choose that branch.
4. Open the GitHub Pages URL shown there and review the site. Leave Custom domain
   empty during this preview. Check history pages, photo galleries and navigation.

The preview URL will normally look like:
https://YOUR-ACCOUNT.github.io/weimar-family-history/

KEEP WEIMARFAMILY.ORG WHEN READY

The domain has not been switched and the existing hosting has not been changed.
templates/CNAME contains weimarfamily.org for the later switch; it is deliberately
outside docs/ so that the GitHub preview does not redirect to the existing host.

1. Verify weimarfamily.org in your GitHub account's Pages settings using the TXT
   record GitHub supplies. Domain registration can stay with the current provider.
2. After the preview passes review, set the repository's Custom domain to
   weimarfamily.org. For branch publishing, GitHub creates docs/CNAME. Keep that
   file in your local copy on future updates; templates/CNAME is the prepared copy.
3. Update the website DNS records using the current official instructions below.
   Configure both weimarfamily.org and www.weimarfamily.org. Preserve the domain
   registration and confirm DNS will remain available after hosting is cancelled.
   The current nameservers are associated with the hosting provider, so DNS may
   need to move to a registrar or another DNS provider before cancellation.
4. Once GitHub offers it, enable Enforce HTTPS. Check both domain forms, existing
   page addresses and a selection of photos. Allow DNS time to settle.
5. Only then cancel the old WEB HOSTING service. Keep DOMAIN REGISTRATION renewing.

GitHub setup:
https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
Domain verification:
https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
Custom domain and DNS:
https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

UPDATING THE SITE

Edit files under docs/ and commit/push the changes. Pages will publish the update.
Keep exact capitalization in filenames and links. Keep links relative (for example,
files/Andrew.jpg) so they work on both the preview URL and the custom domain.

For an optional local check from this repository folder:
python3 tools/check_site.py

For a local preview:
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
Then visit http://127.0.0.1:8765/ and stop the server with Control-C when finished.

See MIGRATION-NOTES.txt for the cleanup details and remaining archival gaps.
