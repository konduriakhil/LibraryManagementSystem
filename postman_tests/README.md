### Step-by-Step Guide to Running Postman Collection from Command Line

#### 1. Install Node.js

First, ensure that Node.js is installed on your machine. You can download and install Node.js from [nodejs.org](https://nodejs.org/). Newman is a Node.js package, so Node.js is required.

#### 2. Install Newman

Once Node.js is installed, you can install Newman using npm (Node Package Manager) by running the following command in your terminal:

```bash
npm install -g newman
```

This command installs Newman globally on your system.


#### 3. Run the Collection with Newman

Use the `newman run` command to execute your Postman collection. Here’s the basic syntax:

```bash
newman run <path-to-collection.json>
```

##### Example Command

```bash
newman run LibraryApplication.postman_collection.json
```

If you need to specify an environment file, you can use the `-e` option:

```bash
newman run collection.json -e localenvironment.json
```

#### 4. Make necessary changes to the environment variables

To set the variables in `localenvironment.json`, you can create a file called `environment.json` with the necessary key-value pairs. Here is an example of how to structure your `environment.json` file:


#### 5. Additional Options for Newman

Newman offers various options to customize the execution:

- **`-r`**: Specify reporters (e.g., `cli`, `html`, `json`).
- **`--timeout`**: Set a global request timeout in milliseconds.
- **`--iteration-count`**: Number of times to run the collection.
- **`--delay-request`**: Specify delay between requests in milliseconds.

##### Example with Additional Options

```bash
newman run collection.json -e environment.json -r cli,html --timeout 10000 --iteration-count 3 --delay-request 2000
```

- **`-r cli,html`**: Uses CLI and HTML reporters to output the results.
- **`--timeout 10000`**: Sets a timeout of 10 seconds per request.
- **`--iteration-count 3`**: Runs the collection 3 times.
- **`--delay-request 2000`**: Delays each request by 2 seconds.

#### 6. Generating HTML Reports (Optional)

If you want a detailed HTML report, ensure Newman HTML Reporter is installed:

```bash
npm install -g newman-reporter-html
```

Then, use the command:

```bash
newman run collection.json -e environment.json -r html
```

This generates an HTML report in the current directory.

### Summary

1. **Install Newman** using npm.
2. **Export your collection** and environment from Postman.
3. **Run the collection** using `newman run` with the desired options.
4. **Customize execution** with additional Newman flags as needed.

Using Newman, you can easily automate your Postman collections from the command line, integrating with CI/CD pipelines or other automation scripts. Let me know if you need further assistance or customization!