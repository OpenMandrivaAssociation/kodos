%define name kodos
%define version 2.4.9
%define release %mkrel 9

Summary: Visual regular expression editor
Name: %{name}
Version: %{version}
Release: %{release}
Source: %{name}-%{version}.tar.bz2
License: GPL
Group: Development/Python
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: PyQt >= 3.0
Url: https://kodos.sourceforge.net

%py_requires -d

BuildRequires: imagemagick
BuildRequires: PyQt

%description
Kodos is a visual regular expression editor and debugger.
It allows you to write python regexp and examine their match.

%prep
%setup -q

%build
rm -Rf $(find . -name '*.ui' | sed 's/ui$/py/' )
# regenerate the ui to be compatible with latest pyqt 
for i in $(find . -name '*.ui'); do
    pyuic $i -o ${i//\.ui/\.py} 
done

python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mv $RPM_BUILD_ROOT/%_bindir/kodos.py $RPM_BUILD_ROOT/%_bindir/kodos

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Kodos
Comment=Visual regular expression editor
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Development;Qt;X-MandrivaLinux-MoreApplications-Development-Tools;
EOF

# non readable in 2.4.9, check if it still cause problem on update
chmod o+r $RPM_BUILD_ROOT/usr/share/kodos/modules/helpBA.ui 

mkdir -p $RPM_BUILD_ROOT/%_iconsdir/
mkdir -p $RPM_BUILD_ROOT/%_miconsdir/
mkdir -p $RPM_BUILD_ROOT/%_liconsdir/

cp ./images/kodos.png $RPM_BUILD_ROOT/%_iconsdir/
convert -size 16x16 ./images/kodos.png $RPM_BUILD_ROOT/%_miconsdir/%name.png
convert -size 64x64 ./images/kodos.png $RPM_BUILD_ROOT/%_liconsdir/%name.png

%if %mdkversion < 200900
%postun
%update_menus
%endif

%if %mdkversion < 200900
%post
%update_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt CHANGELOG.txt
%{_bindir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/%{name}/
%{py_libdir}/site-packages/*
%{_iconsdir}/*png
%{_miconsdir}/*png
%{_liconsdir}/*png




%changelog
* Tue Nov 23 2010 Funda Wang <fwang@mandriva.org> 2.4.9-9mdv2011.0
+ Revision: 599899
- rebuild
- rebuild for py2.7

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 2.4.9-6mdv2009.1
+ Revision: 325683
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 2.4.9-5mdv2009.0
+ Revision: 247813
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.4.9-3mdv2008.1
+ Revision: 170931
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 2.4.9-2mdv2008.1
+ Revision: 140863
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Sat Dec 02 2006 Olivier Thauvin <nanardon@mandriva.org> 2.4.9-2mdv2007.0
+ Revision: 90117
- rebuild

  + Michael Scherer <misc@mandriva.org>
    - Import kodos

* Fri Jul 21 2006 Michael Scherer <misc@mandriva.org> 2.4.9-1mdv2007.0
- New version 2.4.9
- xdg menu

* Fri Sep 30 2005 Michael Scherer <misc@mandriva.org> 2.4.7-1mdk
- New release 2.4.7
- use new python macro
- add changelog

* Thu Aug 25 2005 Michael Scherer <misc@mandriva.org> 2.4.5-5mdk
- fix shared directory

* Fri Jun 03 2005 Michael Scherer <misc@mandriva.org> 2.4.5-4mdk
- mkrel
- reupload to fix missing srpm

* Tue Mar 01 2005 Michael Scherer <misc@mandrake.org> 2.4.5-3mdk
- fix issues with latest pyqt

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 2.4.5-2mdk
- Rebuild for new python

* Fri Aug 27 2004 Michael Scherer <misc@mandrake.org> 2.4.5-1mdk
- first Mandrakelinux package, based on spec made by Phil Schwartz <phil_schwartz@sourceforge.net>.

