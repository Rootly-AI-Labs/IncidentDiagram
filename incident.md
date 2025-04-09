graph TD
  WPCore["Blog"]
  AdminUI["Admin UI<br>wp-admin/"]
  PostNew["New Post<br>post-new.php"]
  FrontEnd["Home page<br>index.php"]
  MediaUpload["Media Library<br>upload.php"]
  SinglePost["Single Article<br>single.php"]
  Comments["Comments with an image<br>comment.php"]
  UploadHandler["Bug: Required 500GB disk space for image upload<br>wp_check_upload_size()<br>in wp-includes/functions.php"]
  WPCore --> AdminUI
  WPCore --> FrontEnd
  AdminUI --> PostNew
  PostNew --> MediaUpload
  FrontEnd --> SinglePost
  SinglePost --> Comments
  UploadHandler -.-> MediaUpload 
  UploadHandler -.-> Comments
  style UploadHandler fill:#ffbf94,stroke:#333,stroke-width:2px,color:#333
  style Comments fill:#ff9496,stroke:#333,stroke-width:2px,color:#333
  style MediaUpload fill:#ff9496,stroke:#333,stroke-width:2px,color:#333
