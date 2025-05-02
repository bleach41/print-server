; Definir el nombre de la aplicación y la versión
!define APPNAME "Print Server"
!define EXECNAME "app"
!define COMPANYNAME "TECOPOS"
!define DESCRIPTION "Servidor de impresión para impresoras térmicas"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

; Incluir librerías modernas de NSIS
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Configuración general
Name "${APPNAME}"
OutFile "PrintServer-Setup.exe"
InstallDir "$PROGRAMFILES\${COMPANYNAME}\${APPNAME}"
InstallDirRegKey HKCU "Software\${COMPANYNAME}\${APPNAME}" ""
RequestExecutionLevel admin

; Páginas del instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas del desinstalador
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Configuración de idioma
!insertmacro MUI_LANGUAGE "Spanish"

Section "Programa Principal" SecMain
    SetOutPath "$INSTDIR"
    
    ; Archivos principales
    File "dist\${EXECNAME}.exe"
    
    ; Crear accesos directos
    CreateDirectory "$SMPROGRAMS\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\${EXECNAME}.exe"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXECNAME}.exe"
    
    ; Escribir información del desinstalador
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Escribir información en el registro
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$\"$INSTDIR\${EXECNAME}.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    
    ; Opcional: Iniciar con Windows
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "${APPNAME}" "$INSTDIR\${EXECNAME}.exe"
SectionEnd

Section "Uninstall"
    ; Eliminar archivos
    Delete "$INSTDIR\${EXECNAME}.exe"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Eliminar accesos directos
    Delete "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${COMPANYNAME}"
    
    ; Eliminar directorio de instalación
    RMDir "$INSTDIR"
    
    ; Eliminar registro
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}"
    DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "${APPNAME}"
    DeleteRegKey /ifempty HKCU "Software\${COMPANYNAME}\${APPNAME}"
SectionEnd 