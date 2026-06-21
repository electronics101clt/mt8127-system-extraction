#!/usr/bin/env python3
"""
Improve generic explanations with detailed descriptions
"""

# Unix/Linux standard utilities
UNIX_COMMANDS = {
    'acpi': 'Display ACPI (power management) information',
    'base64': 'Encode/decode data in base64 format',
    'basename': 'Strip directory path from filename',
    'blockdev': 'Query/set block device properties',
    'cal': 'Display calendar',
    'cat': 'Concatenate and display files',
    'chcon': 'Change SELinux security context',
    'chgrp': 'Change file group ownership',
    'chmod': 'Change file permissions',
    'chown': 'Change file owner and group',
    'chroot': 'Run command with different root directory',
    'chrt': 'Manipulate real-time process scheduling',
    'cksum': 'Calculate CRC checksums',
    'clear': 'Clear terminal screen',
    'cmp': 'Compare two files byte by byte',
    'comm': 'Compare sorted files line by line',
    'cp': 'Copy files and directories',
    'cpio': 'Archive utility for backup/restore',
    'cut': 'Extract columns from files',
    'date': 'Display or set system date and time',
    'dd': 'Convert and copy files (disk duplicator)',
    'df': 'Report filesystem disk space usage',
    'diff': 'Compare files line by line',
    'dirname': 'Strip filename from path',
    'dmesg': 'Display kernel ring buffer messages',
    'dos2unix': 'Convert DOS/Windows line endings to Unix',
    'du': 'Estimate file/directory disk usage',
    'echo': 'Display text to output',
    'egrep': 'Extended grep - search files with regex',
    'env': 'Display or set environment variables',
    'expand': 'Convert tabs to spaces',
    'expr': 'Evaluate expressions',
    'fallocate': 'Preallocate space for files',
    'false': 'Return false exit status',
    'fgrep': 'Fast grep - search for fixed strings',
    'file': 'Determine file type',
    'find': 'Search for files in directory hierarchy',
    'flock': 'Manage file locks',
    'free': 'Display memory usage statistics',
    'getenforce': 'Get current SELinux enforcement mode',
    'getprop': 'Get Android system property value',
    'grep': 'Search text using patterns',
    'groups': 'Display user group memberships',
    'gunzip': 'Decompress gzip files',
    'gzip': 'Compress files using gzip',
    'head': 'Display first lines of file',
    'hostname': 'Display or set system hostname',
    'id': 'Display user/group ID information',
    'ifconfig': 'Configure network interface',
    'insmod': 'Insert kernel module',
    'ip': 'Show/manipulate routing and network devices',
    'iptables': 'IPv4 packet filtering and NAT',
    'kill': 'Send signal to process',
    'ln': 'Create links between files',
    'logcat': 'View Android system logs',
    'losetup': 'Setup loop devices',
    'ls': 'List directory contents',
    'lsmod': 'List loaded kernel modules',
    'lsof': 'List open files and processes',
    'lsusb': 'List USB devices',
    'md5sum': 'Calculate MD5 checksums',
    'mkdir': 'Create directories',
    'mke2fs': 'Create ext2/ext3/ext4 filesystem',
    'mkfs': 'Build a filesystem',
    'mknod': 'Create special files (device nodes)',
    'mkswap': 'Setup swap area',
    'mktemp': 'Create temporary file or directory',
    'more': 'Page through text files',
    'mount': 'Mount filesystem',
    'mv': 'Move or rename files',
    'nc': 'Netcat - network utility for TCP/UDP',
    'netstat': 'Network statistics and connections',
    'nice': 'Run program with modified priority',
    'nohup': 'Run command immune to hangups',
    'od': 'Dump files in octal/other formats',
    'paste': 'Merge lines of files',
    'patch': 'Apply diff patch to files',
    'ping': 'Send ICMP ECHO_REQUEST to network hosts',
    'ping6': 'Send ICMPv6 ECHO_REQUEST',
    'pkill': 'Kill processes by name',
    'printenv': 'Print environment variables',
    'printf': 'Format and print data',
    'ps': 'Report process status',
    'pwd': 'Print working directory',
    'readlink': 'Display symlink target',
    'reboot': 'Reboot the system',
    'renice': 'Change process priority',
    'rm': 'Remove files or directories',
    'rmdir': 'Remove empty directories',
    'rmmod': 'Remove kernel module',
    'route': 'Show/manipulate IP routing table',
    'sed': 'Stream editor for text transformation',
    'seq': 'Generate sequence of numbers',
    'setenforce': 'Set SELinux enforcement mode',
    'setprop': 'Set Android system property',
    'sh': 'Shell command interpreter',
    'sha1sum': 'Calculate SHA1 checksums',
    'sha256sum': 'Calculate SHA256 checksums',
    'sleep': 'Delay for specified time',
    'sort': 'Sort lines of text',
    'stat': 'Display file/filesystem status',
    'strings': 'Extract printable strings from files',
    'stty': 'Change/print terminal settings',
    'su': 'Switch user or become superuser',
    'swapon': 'Enable swap space',
    'swapoff': 'Disable swap space',
    'sync': 'Flush filesystem buffers to disk',
    'sysctl': 'Configure kernel parameters at runtime',
    'tail': 'Display last lines of file',
    'tar': 'Archive utility for tape archives',
    'taskset': 'Set/retrieve CPU affinity',
    'tc': 'Traffic control for network QoS',
    'tee': 'Read stdin and write to stdout and files',
    'test': 'Evaluate conditional expressions',
    'time': 'Time command execution',
    'timeout': 'Run command with time limit',
    'top': 'Display running processes',
    'touch': 'Update file timestamps',
    'tr': 'Translate or delete characters',
    'true': 'Return true exit status',
    'truncate': 'Shrink or extend file size',
    'tty': 'Print terminal name',
    'umount': 'Unmount filesystem',
    'uname': 'Print system information',
    'uniq': 'Remove duplicate lines',
    'unix2dos': 'Convert Unix line endings to DOS/Windows',
    'unzip': 'Extract compressed ZIP archives',
    'uptime': 'Show system uptime',
    'usleep': 'Sleep for microseconds',
    'wc': 'Count lines, words, bytes in files',
    'which': 'Locate command in PATH',
    'whoami': 'Print effective user name',
    'xargs': 'Build and execute commands from stdin',
    'yes': 'Output string repeatedly',
    'zip': 'Create ZIP compressed archives',
}

# /proc specific entries (detailed)
def explain_proc_entry(path):
    """Detailed explanations for /proc entries"""

    # Generic patterns
    if '/task/' in path:
        if '/attr/current' in path:
            return 'SELinux security context for this thread'
        elif '/attr/prev' in path:
            return 'Previous SELinux security context'
        elif '/attr/exec' in path:
            return 'SELinux context for next exec()'
        elif '/attr/fscreate' in path:
            return 'SELinux context for file creation'
        elif '/attr/keycreate' in path:
            return 'SELinux context for key creation'
        elif '/attr/sockcreate' in path:
            return 'SELinux context for socket creation'
        elif path.endswith('/cgroup'):
            return 'Control group membership for this thread'
        elif path.endswith('/loginuid'):
            return 'Login UID for audit purposes'
        elif path.endswith('/sessionid'):
            return 'Session ID for audit system'
        elif path.endswith('/make-it-fail'):
            return 'Fault injection control (testing)'
        elif path.endswith('/io'):
            return 'I/O statistics for this thread'
        elif path.endswith('/limits'):
            return 'Resource limits (RLIMIT) for this thread'
        elif path.endswith('/oom_score'):
            return 'OOM killer score (higher = more likely to be killed)'
        elif path.endswith('/oom_adj'):
            return 'OOM adjustment value (legacy)'
        elif path.endswith('/oom_score_adj'):
            return 'OOM score adjustment (-1000 to 1000)'
        elif path.endswith('/cpuset'):
            return 'CPU affinity cpuset for this thread'
        elif path.endswith('/stat'):
            return 'Thread statistics - CPU time, state, priority'
        elif path.endswith('/statm'):
            return 'Thread memory usage statistics'
        elif path.endswith('/maps'):
            return 'Memory map - virtual memory regions'
        elif path.endswith('/smaps'):
            return 'Detailed memory map with usage stats'
        elif path.endswith('/numa_maps'):
            return 'NUMA memory allocation information'

    # Process-level (/proc/PID/)
    if path.count('/') >= 2:
        parts = path.split('/')
        if len(parts) > 2 and parts[2].isdigit():
            if '/fd' in path and path.split('/fd')[-1]:
                return 'File descriptor - reference to open file/socket/pipe'
            elif '/fdinfo' in path:
                return 'File descriptor information - flags and position'
            elif '/net/tcp' in path or '/net/tcp6' in path:
                return 'TCP connections - local/remote addresses, state, queues'
            elif '/net/udp' in path or '/net/udp6' in path:
                return 'UDP sockets - local/remote addresses, state'
            elif '/net/raw' in path or '/net/raw6' in path:
                return 'Raw IP sockets'
            elif '/net/unix' in path:
                return 'Unix domain sockets - IPC connections'
            elif '/net/packet' in path:
                return 'Packet sockets - raw Ethernet access'
            elif '/net/route' in path:
                return 'IPv4 routing table entries'
            elif '/net/arp' in path:
                return 'ARP cache - IP to MAC address mappings'
            elif '/net/dev' in path:
                return 'Network device statistics - packets, bytes, errors'
            elif '/net/wireless' in path:
                return 'Wireless network device statistics'
            elif '/net/if_inet6' in path:
                return 'IPv6 network interface addresses'
            elif '/net/ip6_tables_names' in path:
                return 'Loaded IPv6 netfilter tables'
            elif '/net/ip_tables_names' in path:
                return 'Loaded IPv4 netfilter tables'

    # Global /proc entries
    if path == '/proc/buddyinfo':
        return 'Memory fragmentation info - free block sizes'
    elif path == '/proc/cgroups':
        return 'Control group subsystem information'
    elif path == '/proc/consoles':
        return 'Registered system console devices'
    elif path == '/proc/crypto':
        return 'Installed crypto algorithms'
    elif path == '/proc/diskstats':
        return 'Disk I/O statistics per device'
    elif path == '/proc/dma':
        return 'Registered DMA channels'
    elif path == '/proc/execdomains':
        return 'Execution domains (ABI personalities)'
    elif path == '/proc/fb':
        return 'Framebuffer devices'
    elif path == '/proc/iomem':
        return 'Physical memory map - device memory regions'
    elif path == '/proc/ioports':
        return 'I/O port regions registered by drivers'
    elif path == '/proc/kallsyms':
        return 'Kernel symbol table - function addresses'
    elif path == '/proc/kcore':
        return 'Kernel memory image (for debugging)'
    elif path == '/proc/key-users':
        return 'Kernel key management users'
    elif path == '/proc/keys':
        return 'Kernel keyring contents'
    elif path == '/proc/kmsg':
        return 'Kernel messages buffer'
    elif path == '/proc/kpagecount':
        return 'Page reference counts'
    elif path == '/proc/kpageflags':
        return 'Page flags information'
    elif path == '/proc/locks':
        return 'File locks currently held'
    elif path == '/proc/mdstat':
        return 'Software RAID status'
    elif path == '/proc/misc':
        return 'Miscellaneous device drivers'
    elif path == '/proc/pagetypeinfo':
        return 'Memory page type and fragmentation info'
    elif path == '/proc/slabinfo':
        return 'Kernel slab allocator statistics'
    elif path == '/proc/softirqs':
        return 'Software interrupt statistics'
    elif path == '/proc/timer_list':
        return 'Active kernel timers'
    elif path == '/proc/vmallocinfo':
        return 'vmalloc memory allocation info'
    elif path == '/proc/vmstat':
        return 'Virtual memory statistics'
    elif path == '/proc/zoneinfo':
        return 'Memory zone information'

    return None

def improve_line(line):
    """Improve a single line's explanation"""
    if ' | ' not in line:
        return line

    path, explanation = line.strip().split(' | ', 1)
    basename = path.split('/')[-1]

    # Unix commands
    if explanation.startswith('Vendor binary:') or explanation.startswith('Unknown system binary:'):
        if basename in UNIX_COMMANDS:
            return f"{path} | {UNIX_COMMANDS[basename]}"

    # /proc improvements
    if path.startswith('/proc'):
        better = explain_proc_entry(path)
        if better:
            return f"{path} | {better}"

    # Directory improvements
    if explanation.startswith('Directory:'):
        # App directories
        if path.endswith(('/ApplicationsProvider', '/AtciService', '/BookmarkProvider')):
            app_name = basename
            return f"{path} | Application package directory for {app_name}"
        # Specific system directories
        elif basename in ['soundfx', 'vndk', 'vndk-sp', 'vendor']:
            if basename == 'soundfx':
                return f"{path} | Audio effects library directory"
            elif basename == 'vndk':
                return f"{path} | Vendor Native Development Kit libraries"
            elif basename == 'vndk-sp':
                return f"{path} | VNDK Same-Process libraries"
        # Lib subdirs
        elif path.endswith('/egl'):
            return f"{path} | EGL (OpenGL ES interface) library directory"
        elif path.endswith('/drm'):
            return f"{path} | DRM (Digital Rights Management) library directory"

    # /sys improvements
    if path.startswith('/sys') and (explanation == 'Kernel device/driver information' or
                                    explanation.startswith('Kernel device/driver')):
        if '/devices/platform/' in path:
            return f"{path} | Platform device - SoC integrated hardware"
        elif '/devices/virtual/' in path:
            return f"{path} | Virtual device - kernel software device"
        elif '/devices/system/' in path:
            if '/cpu/' in path:
                return f"{path} | CPU core properties and control"
            else:
                return f"{path} | System device properties"
        elif '/class/power_supply/' in path:
            return f"{path} | Power supply/battery properties"
        elif '/class/thermal/' in path:
            return f"{path} | Thermal zone temperature and limits"
        elif '/class/backlight/' in path:
            return f"{path} | Display backlight brightness control"
        elif '/class/leds/' in path:
            return f"{path} | LED control - brightness, trigger"
        elif '/bus/platform/' in path:
            return f"{path} | Platform bus - SoC integrated devices"
        elif '/module/' in path:
            return f"{path} | Kernel module parameters and info"

    return line

# Main processing
print("Improving explanations...")
with open('device-tree-annotated.txt', 'r') as f:
    lines = f.readlines()

output = []
improved_count = 0

for i, line in enumerate(lines):
    if i % 50000 == 0:
        print(f"  Progress: {i}/{len(lines)}")

    new_line = improve_line(line)
    if new_line != line:
        improved_count += 1
    output.append(new_line)

print(f"\nWriting improved file...")
with open('device-tree-annotated.txt', 'w') as f:
    f.writelines(output)

print(f"Done! Improved {improved_count} explanations")
PYEOF
