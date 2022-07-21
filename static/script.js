render();
function render() {
  document
    .getElementById("myFile")
    .addEventListener("change", handleFileSelect, false);
}

function handleFileSelect() {
const reader = new FileReader();
console.log(reader)
// const image = render.result

  // fetch('https://neeldemo-dot-applied-ai-labs.uc.r.appspot.com/', {
  //   method: 'post',
  //   body: JSON.parse({image})
  // }).then(response=>{
  //   if(response.ok) return response.json()
  //   return response.json().then(json=>Promise.reject(json))
  // }).then(json => {

  //   //process

  // }).catch(error =>{
  //   console.error(error)
  // })
  
  
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    removeUploadIcon()
    
    if(uploaded_image.includes('pdf')){
      const __div__ =  document.querySelector('#preview')
      __div__.style.backgroundImage = `url('')`
      const __iframe__ = document.createElement('iframe')
      __iframe__.src = `${uploaded_image}`
      __iframe__.classList.add('pdf-viewer')

      __div__.appendChild(__iframe__)
    }else{
      const __previewDiv__ = document.getElementById('preview')
      if(__previewDiv__.hasChildNodes()){
        __previewDiv__.removeChild(__previewDiv__.firstChild)
      }

      __previewDiv__.style.backgroundImage = `url(${uploaded_image})`
      }
  })
  reader.readAsDataURL(this.files[0]);
}
function removeUploadIcon(){
  const __div__ =  document.querySelector('#preview')
    __div__.removeChild(__div__.firstChild)
}