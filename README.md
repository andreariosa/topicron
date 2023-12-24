# Introduction

[TopiCron](https://topicron.com/) is my open source project that serves as a "playground" where I can experiment, keep up to date with new technologies and quickly access resources that might be useful.

## What you find here

### Core

Next.js project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) containing:

- An [app router](https://nextjs.org/learn) version of the [pages router](https://nextjs.org/learn-pages-router) tutorial for building a simple [blog](https://github.com/vercel/next-learn/tree/main/basics/demo).
- An RSS parser.

# Getting Started

After cloning the repository open a terminal window, go into the root project folder and run: `npm install`.

## Run the Development Server

```bash
npm run dev
```

Then, visit [http://localhost:3000](http://localhost:3000) with a browser.

# Dependencies

| Package name | Link | Size | Import |
| - | - | - | - |
| `gray-matter` | [npm](https://www.npmjs.com/package/gray-matter) | [bundlephobia](https://bundlephobia.com/package/gray-matter) | **Blog** lib |
| `remark` | [npm](https://www.npmjs.com/package/remark) | [bundlephobia](https://bundlephobia.com/package/remark) | **Blog** lib |
| `remark-html` | [npm](https://www.npmjs.com/package/remark-html) | [bundlephobia](https://bundlephobia.com/package/remark-html) | **Blog** lib |
| `rss-parser` | [npm](https://www.npmjs.com/package/rss-parser) | [bundlephobia](https://bundlephobia.com/package/rss-parser) | **RSS** lib |
| `date-fns` | [npm](https://www.npmjs.com/package/date-fns) | [bundlephobia](https://bundlephobia.com/package/date-fns) | **Blog** + **RSS** components |

# Best Practices

## Module dependencies ordering

| Keyword  | Description                                            |
| -------- | ------------------------------------------------------ |
| Builtin  | Standard libraries                                     |
| External | Third party libraries                                  |
| Internal | Own code imports                                       |
| Specific | Imports specific to the module (e.g. css, png, etc.)   |
| Test     | Code only used for tests                               |

## Subject line terminology for committing

| First Word | Meaning                                              |
| ---------- | ---------------------------------------------------- |
| Add        | Create a capability e.g. feature, test, dependency.  |
| Cut        | Remove a capability e.g. feature, test, dependency.  |
| Fix        | Fix an issue e.g. bug, typo, accident, misstatement. |
| Bump       | Increase the version of something e.g. dependency.   |
| Make       | Change the build process, or tooling, or infra.      |
| Start      | Begin doing something e.g. create a feature flag.    |
| Stop       | End doing something e.g. remove a feature flag.      |
| Refactor   | A code change that MUST be just a refactoring.       |
| Reformat   | Refactor of formatting e.g. omit white space.        |
| Optimize   | Refactor of performance e.g. speed up code.          |
| Document   | Refactor of documentation e.g. help files.           |

## Accidentally pushed to main

1. Don't panic.
2. If you are not sure what you'll going to do, ask for help.
3. For reverse to the last commit `git reset --hard HEAD~1`.
4. For reverse to a specific commit `git reset --hard <SHA> (ex. git reset --hard 3ffd44f)`.
5. Then do `git push origin +main --force`.
6. Remember to also fix the commits on the production repository.

# Documentation references

- GitHub: https://docs.github.com/en
- Visual Studio Code: https://code.visualstudio.com/docs
- NextJS: https://nextjs.org/docs
- TailwindCSS: https://tailwindcss.com/docs
