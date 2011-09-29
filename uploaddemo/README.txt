This demo shows two ways of handling file upload progress. The first
is using Django code to track and report upload progress. This needs
custom upload handlers and a report view.

The second is to let a front-end proxy like nginx or lighttpd handle
the upload and take care of reporting progress back to the AJAX
client. The advantage here, of course, is that big Django processes
aren't tied up handling uploads. The proxy can receive the file in its
entirety before sending it to Django over a much faster local socket.

The premise of the demo is that you have admin staff uploading files,
but they're stored under MEDIA_ROOT and accessible to everyone. If you
want authenticated downloads, there's more involved. I handle it with
custom views that store uploads in a protected directory and delegate
the actual file delivery to nginx via its X-Accel-Redirect feature;
this could also be done with Apache via mod_xsendfile, or with
lighttpd's X-Sendfile support.

Trying it out
-------------

It's mostly intended as sample code, but I have tested this demo app
under Apache/mod_wsgi and nginx/FastCGI. To try it yourself, first run
'./manage.py syncdb' in the demo app directory to create the database.
Remember the superuser and password; you'll use them when testing
uploads.

Then you need to configure your web server. Under Apache/mod_wsgi,
just include the supplied apache.conf in your Apache configuration,
adjusting paths and ports as necessary.

To try it with nginx, add the supplied nginx.conf to your nginx
config, then use start-server.sh to start the FastCGI server. Again,
you may need to change paths and port numbers.

That should be it. Browse to the demo site and try some uploads, and
of course if you have any questions, feel free to get in touch with
me via http://www.fairviewcomputing.com/.


For Apache mod_wsgi
------------------
1. tar zxf mod_wsgi-3.3.tar.gz
2. cd mod_wsgi-3.3
3. read README. 
may need to install apache devel package, try like: yum install httpd-devel.
if yum installs yum install apr-devel..i386, manually install: yum install
apr-devel.x86_64.
4. chmod 777 ./db, ./db/uploaddemo.db, ./media for http to access

more references:
http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide
