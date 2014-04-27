  module.exports = function(grunt) {
  defaultTasks = ['clean', 'jshint', 'less', 'copy', 'jinja:md', 'markdown',
    'jinja:pages']; // 'htmlmin'

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      files: ['Gruntfile.js', 'src/**/*.js'],
      options: {
        // options here to override JSHint defaults
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true,
        },
        ignores: "**/*min.js"
      }
    },
    less: {
      options: {
          paths: ['src/assets/styles/*.less'],
          report: 'gzip',
          cleancss: true
      },
      src: {
          expand: true,
          cwd:    "src/assets/styles",
          src:    "*.less",
          dest:   "build/assets/styles",
          ext:    ".css"
      }
    },
    copy: {
      files: {
        expand: true,
        cwd: 'src/',
        src: ['**', '!**/*.less', '!**/*.html', '!**/*.md'],
        dest: 'build/',
        //ignores: ['**/*.js', '**/*.css'],
        mode: 0644,
      }
    },
    watch: {
      default: {
        files: ['src/**', 'Gruntfile.js'],
        tasks: defaultTasks,
        options: {
          spawn: false,
          atBegin: true
        },
      },
    },
    clean: ['build', 'tmp'],
    // htmlmin: {
    //   options: {
    //     removeComments: true,
    //     collapseWhitespace: true
    //   },
    //   files: {
    //     expand: true,
    //     cwd: 'src/',
    //     src: ['**/*.html', '!**/*.jinja.html', '!**/_*.html'],
    //     dest: 'build/'
    //   }
    // },
    rsync: {
      options: {
        recursive: true
      },
      prod: {
        options: {
          src: "build/",
          dest: "/var/www/https/hugo.barrera.io/",
          host: "root@elysion.barrera.io",
          syncDestIgnoreExcl: true
        }
      },
    },
    'http-server': {
      local: {
        root: 'build',

        port: 8090,
        host: "0.0.0.0",

        cache: 0,
        showDir: false,
        autoIndex: true,
        defaultExt: 'html',
        runInBackground: true
      }
    },
    jinja: {
      md : {
        options: {
          templateDirs: ['src'],
          contextRoot: 'src/'
        },
        files: [{
          expand: true,
          dest: 'tmp/',
          cwd: 'src/',
          src: ['**/!(_)*.md']
        }]
      },
      pages : {
        options: {
          // tmp takes precedence, since that has some preprocessed files
          templateDirs: ['tmp', 'src'],
          contextRoot: 'src/'
        },
        files: [{
          expand: true,
          dest: 'build/',
          cwd: 'tmp/',
          src: ['**/!(_)*.html'],
          rename: function (dest, src, opts) {
            if (src.split("/").pop() == "index.html")
              return dest + src;
            var arr = src.split(".");
            arr.pop();
            return dest + arr.join("") + "/index.html";
          }
        }]
      }
    },
    markdown: {
      all: {
        files: [
          {
            expand: true,
            // Move to tmp since we can do jinja templating for variables there
            dest: 'tmp',
            cwd: 'tmp/',
            src: '**/*.md',
            ext: '.html'
          }
        ]
      },
      options: {
        template: 'src/_base.html',
        markdownOptions: {
          gfm: true,
          highlight: "auto",
          codeLines: {
            before: '<span>',
            after: '</span>'
          }
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-htmlmin');
  grunt.loadNpmTasks("grunt-rsync");
  grunt.loadNpmTasks("grunt-http-server");
  grunt.loadNpmTasks("grunt-jinja");
  grunt.loadNpmTasks('grunt-markdown');

  grunt.registerTask('test', ['jshint']);
  grunt.registerTask('default', defaultTasks);
  grunt.registerTask('deploy', defaultTasks.concat(['rsync']));
  grunt.registerTask('serve', ['http-server', 'watch']);
};
