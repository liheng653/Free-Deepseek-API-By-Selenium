# Free-Deepseek-API-By-Selenium
Simulate using Deepseek on website by selenium, packed as free API for wider usages,e.g. quick search,automate online work.

### How to Use

#### Create an Instance

`deepseek = Deepseek("15915091250","Liheng1123581321")`

#### Send Message

`print(deepseek.send('Hello

The answer from Deepseek will be printed after its output completes.

#### Mode

`deepseek.setDeepThink(False)
deepseek.setSearch(True)
`

#### Upload File

`deepseek.uploadFile(file_path)`

#### Chat History

`deepseek.history`

A list object containing dict objects.Format:

`[{'user':'Hello!','ds':'Hello!How can I help you today?'},{...},...]`
