import os
import plistlib

version = os.getenv('BUILD_VERSION', None)
print('version: %s' % version)

commit = os.getenv('GITHUB_SHA', 'development build')
print('commit: %s' % commit)

if not version:
    checked = '<i class="fas fa-fw fa-times-circle" style="color:red"></i>'
    if commit != 'development build':
        version = commit[0:7]
        print('using commit as version: %s' % version)
    else:
        version = commit
        print('unknown version: %s' % version)
else:
    checked = '<i class="fas fa-fw fa-check-circle" style="color:green"></i>'

info_file = os.path.join('Contents', 'Info.plist')

pl = dict(
    CFBundleIdentifier='dev.lizardbyte.plexhints',
    PlexAgentAttributionText="""
        <![CDATA[
            <!-- Import custom css -->
            <style>
                @import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");
            </style>
            <style>
                div.center {
                    text-align: center;
                }
            </style>

            <div class="center">
                <strong>plexhints</strong><br>
            </div>
            <br>
            A plugin by <a href="https://app.lizardbyte.dev" target="_blank">LizardByte</a> used to plugin
            developers with CI/CD workflows.
            <br>
            <br>
            <table>
                <tr>
                    <td>Version:  %s</td>
                    <td>%s</td>
                    <td>| <a href="https://github.com/LizardByte/plugins/releases/latest"
                             target="_blank">Releases</a></td>
                </tr>
            </table>
            <br>
            <table>
                <tr>
                    <td><i class="fa fa-fw fa-question-circle"></i> Reference:</td>
                    <td>| <i class="fas fa-fw fa-file-lines"></i> <a
                            href="https://docs.lizardbyte.dev/projects/plexhints" target="_blank">Docs</a></td>
                </tr>
            </table>
            <br>
            <div class="center">
                <i class="fab fa-fw fa-python" style="font-size:80px;"></i>
            </div>

            <script>
                <!-- Custom Javascript here -->
            </script>
        ]]>
    """ % (checked, version),
    CFBundleDevelopmentRegion='English',
    CFBundleExecutable='',
    CFBundlePackageType='AAPL',
    CFBundleSignature='hook',
    PlexFrameworkVersion='2',
    PlexClientPlatforms='',
    PlexClientPlatformExclusions='',
    PlexPluginClass='Resource',
    PlexPluginCodePolicy='Elevated',
    PlexPluginConsoleLogging='0',
    PlexPluginDebug='1',
    PlexPluginMode='Daemon',
    PlexPluginRegions=[''],
    PlexBundleVersion=version,
    PlexShortBundleVersion=version,
)

# PlexPluginMode:
# This one does nothing with a value of "Always On", a value of "daemon" keeps the plugin alive in the background.

# PlexClientPlatforms and PlexClientPlatformExclusions:
# Any Clients support or not supported by the plugin.
# Possible values are * for all platforms, MacOSX, Windows, Linux, Roku, Android, iOS, Safari, Firefox, Chrome, LGTV, \
# Samsung, PlexConnect and Plex Home Theater

# PlexPluginRegions:
# Possible string values are the proper ISO two-letter code for the country.
# A full list of values are available at http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

# PlexPluginDebug:
# Possible values are 0 and 1. Setting it to "1" rather than "0" turns on debug logging

# PlexPluginCodePolicy:
# This allows channels to access some python methods which are otherwise blocked, as well as import external code \
# libraries, and interact with the PMS HTTP API

# PlexPluginClass:
# This key is used to show that the plugin is an agent. possible values are 'Agent' and 'Resource'

# PlexPluginConsoleLogging:
# This is used to send plugin log statements directly to stout when running PMS from the command line. \
# Rarely used anymore

try:
    plist_string = plistlib.writePlistToString(pl).replace('&lt;', '<').replace('&gt;', '>')
except AttributeError:
    plist_string = plistlib.dumps(pl).decode('utf-8').replace('&lt;', '<').replace('&gt;', '>').encode('utf-8')

with open(info_file, 'wb') as fp:
    fp.write(plist_string)
