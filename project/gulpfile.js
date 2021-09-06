var gulp        = require('gulp');
var browserSync = require('browser-sync').create();
var sass        = require('gulp-sass')(require('sass'));

// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function() {
    return gulp.src("static/scss/*.scss")
        .pipe(sass())
        .pipe(gulp.dest("static/css"))
        .pipe(browserSync.stream());
});

// Static Server + watching scss/html files
gulp.task('serve', gulp.series('sass', function() {

    browserSync.init({
        server: "./templates/"
    });

    gulp.watch("static/scss/*.scss", gulp.series('sass'));
    gulp.watch("static/templates/*.html").on('change', browserSync.reload);
}));

gulp.task('default', gulp.series('serve'));