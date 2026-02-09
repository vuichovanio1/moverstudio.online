$files = @(
    "index.html",
    "sait-vizitka.html",
    "calculator.html",
    "case-studies.html",
    "dokazatelstva.html",
    "how-we-do-it.html",
    "izrabotka-na-sait.html",
    "pagespeed-100-html.html",
    "seo-optimizacia.html",
    "wordpress-alternativa.html",
    "blog\5-prichini-da-napusnesh-wordpress-dnes.html",
    "blog\zashto-wordpress-e-baven.html"
)

foreach ($file in $files) {
    $path = "c:\Users\MacMic\source\repos\moverstudio.online\$file"
    if (Test-Path $path) {
        $content = Get-Content $path -Raw -Encoding UTF8
        # Replace url(" with url('
        $content = $content -replace 'url\("data:image/svg\+xml,', "url('data:image/svg+xml,"
        # Replace "); at end with ');
        $content = $content -replace '%3E"\);', "%3E');"
        # Replace xmlns=' with xmlns="
        $content = $content -replace "xmlns='([^']+)'", 'xmlns="$1"'
        # Replace x=' with x="
        $content = $content -replace " x='", ' x="'
        # Replace y=' with y="
        $content = $content -replace " y='", ' y="'
        # Replace width=' with width="
        $content = $content -replace " width='", ' width="'
        # Replace height=' with height="
        $content = $content -replace " height='", ' height="'
        # Fix closing tags
        $content = $content -replace "'%3E", '"%3E'
        
        $content | Set-Content $path -NoNewline -Encoding UTF8
        Write-Host "Fixed: $file" -ForegroundColor Green
    }
}

Write-Host "`nAll files fixed!" -ForegroundColor Cyan
