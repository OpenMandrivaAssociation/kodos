%define name kodos
%define version 2.4.9
%define release %mkrel 2

Summary: Kodos is a visual regular expression editor
Name: %{name}
Version: %{version}
Release: %{release}
Source: %{name}-%{version}.tar.bz2
License: GPL
Group: Development/Python
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: PyQt >= 3.0
Url: http://kodos.sourceforge.net

%py_requires -d

BuildRequires: ImageMagick
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
Encoding=UTF-8
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

%postun
%update_menus

%post
%update_menus

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


