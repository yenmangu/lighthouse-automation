# StudyStack - Community Resource Library

## Overview

## Glossary

## UX

### The 5 Planes of UX

#### 1. Strategy Plane

> This section sets out StudyStack’s core purpose, audience, and user goals. All product decisions are based on addressing real-world needs, ensuring the app delivers practical value to its intended users.

**Purpose**
StudyStack is a ..

**Business/User Goals**

**Primary User Needs**

#### 2. Scope Plane

> Here, StudyStack’s functional scope and content requirements are defined. Features are prioritised using MoSCoW methodology, ensuring the project delivers essential value first while clearly outlining future enhancements.

**Features**

**Future Features (Could-Have)**

**Content Requirements**

#### 3. Structure Plane

> This section explains StudyStack’s information architecture and user flows. Navigation, hierarchy, and page structure are planned to support intuitive, seamless journeys so users always know where they are and what to do next.

**Information Architecture**

- **Page Hierarchy:**

_User Flow_

1.
2.

---

#### 4. Skeleton Plane

> The Skeleton Plane documents StudyStack’s wireframes and component layouts, demonstrating how core features and workflows are physically arranged on each screen. Mobile-first responsive design ensures all layouts adapt gracefully to any device.

##### Wireframe Suggestions

**Wireframes & Layout**

## Wireframes

> **Wireframes were created in [Figma/Mockflow/etc.] and closely followed throughout the build. Design changes made during development are documented in the README.**

#### 5. Surface Plane

> This section explains StudyStack’s visual design system, including colour palette, typography, imagery, interactivity, and support for modern features like dark mode. Each element is selected and tested for clarity, accessibility, and brand consistency.

##### Visual Design Elements

- **Dark Mode Support:**
  - StudyStack respects users’ system dark mode preferences.
  - When the browser is set to dark mode (`prefers-color-scheme: dark`), a dark colour palette is automatically applied for reduced eye strain and better accessibility in low-light environments.
  <!-- - Colours and backgrounds are blended using CSS custom properties and `color-mix` for smooth transitions between themes. -->

### Colour Scheme

I used [the favicon]() along with a colour picker tool to choose the StudyStack colour palette.

> Note about colour inspiration

| Tone | Hex | HSL | Use |
| ---- | --- | --- | --- |

I used [Coolors]() to generate the following pallete from my chosen colours.
![screenshot]()

### Typography

### Imagery

- High-quality, attribution-checked food photography, all with descriptive alt text

  > see [Credits](#foodstock-images--icons) for specific attribution.

### Interactivity & Feedback

- Buttons/links have visible hover/active states and ARIA labels
- “Liked”/“favourited” status is animated for positive feedback
- Error states and loading are clearly communicated to users

**Accessibility Commitment**

- Colour contrast meets or exceeds WCAG 2.1 AA where possible
- All navigation and controls are fully keyboard-accessible
- ARIA labels, roles, and focus indicators are included for all interactive elements

## User Stories

| Target | Expectation | Outcome |
| ------ | ----------- | ------- |

## Features

### **MoSCoW** Prioritisation

Using the **Must-Have**, **Should-Have**, **Could-Have** and **Won't-Have** prioritisation method, the user stories are prioritised in order to better manage the time and resources of the project effectively.

I've decomposed my Epics into User Stories for prioritizing and implementing them. Using this approach, I was able to apply "MoSCow" prioritization and labels to my User Stories within the Issues tab.

- **Must Have**: guaranteed to be delivered - required to Pass the project (_max ~60% of stories_)
- **Should Have**: adds significant value, but not vital (_~20% of stories_)
- **Could Have**: has small impact if left out (_the rest ~20% of stories_)
- **Won't Have**: not a priority for this iteration - future features

### Existing Features

#### User Facing Features

#### Development Features

#### Key References

## Architecture

> StudyStack is architected as a modular, component-driven application, using Django for templating and Bootstrap for responsive design. The application’s structure is deliberately organised to maximise maintainability, reusability, and testability—enabling future features and team development.

### High-Level Overview

## Design Patterns

> Note about design patterns used

### Architecture Overview

### Error Handling Architecture

### Security & Best Practice

### Test & Development Support

### Example Request Flow

### Source Code

## Development & Code Style

> StudyStack is developed with a focus on maintainability, clarity, and modern best practices. Code is written to be self-documenting, with strong adherence to community conventions for version control, structure, and naming.

### GIT

We follow the [Conventional Commits](COMMIT_CONVENTIONS.md) specification.
This ensures all commits are consistent, scoped, and easy to scan.

> Note: Conventional Commits were adopted from 10 September 2025. Earlier commit messages may not follow this format.

### Python

> Note: Note about Python best practices etc

### JavaScript

All JavaScript in StudyStack uses modern [ES Module syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) (`import`/`export`) for modularity and maintainability.

- **Style conventions:**
  - Lower camelCase for variables, functions, and files (no spaces or capitals for cross-platform safety).
  - Functions and classes are documented with [JSDoc](https://jsdoc.app/) for strong IntelliSense and code navigation in VS Code.
  - All major architectural patterns (store, emitter, service) are fully typed and documented.
  - No build tools or transpilers are used; the codebase targets modern browsers (see [Browser Compatibility](#browser-compatibility)).
- **Separation of concerns:**
  - Logic, view rendering, and services are kept in separate modules for each component or slice.

### HTML

- All HTML is written in semantic, accessible markup.
- Components are structured using appropriate tags (`<main>`, `<nav>`, `<header>`, `<section>`, `<article>`, etc.).
- ARIA roles and labels are included where necessary for screen readers and assistive tech.
- No inline styles or scripts; all behaviour and styling is in linked external files.

> **Exception:**
> For technical reasons, certain parts of the app (such as the responsive header system) programmatically apply inline styles directly to `document.documentElement` (the `<html>` tag) at runtime.
> This is necessary for responsive scroll animation and to ensure CSS variables are synchronised across viewport and header changes—techniques which cannot be fully achieved via static CSS alone.
> All such inline styles are set and managed via dedicated JavaScript modules (e.g., `responsiveHeader.js`), and are removed or updated as needed to avoid style conflicts or memory leaks.

> [!NOTE]
> Any inline styles added programmatically are reset and restored on page changes to ensure a consistent and maintainable DOM. This prevents style accumulation or memory leaks and preserves cross-page visual integrity.

### CSS

All custom CSS adopts the BEM (Block, Element, Modifier) naming convention for modular, maintainable styles.

**Benefits:**

- Styles are easy to read and understand
- Modular and reusable across different pages or components
- Resistant to conflicts caused by global class names

#### BEM Naming Convention

**BEM** stands for:

- **Block** - The standalone component (`recipe-card`)
- **Element** - A child part of that component (`recipe-card__title`)
- **Modifier** - A variation of the block or element (`recipe-card--featured`)

```

.block {}
.block\_\_element {}
.block--modifier {}

```

#### Example

> Provide example of actual BEM used in project

## Tools and Technologies

| Tool / Tech                                                                                                             | Use                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [![badge](https://img.shields.io/badge/Markdown_Builder-grey?logo=markdown&logoColor=000000)](https://markdown.2bn.dev) | Creating structured README and TESTING documentation.                                                                           |
| [![badge](https://img.shields.io/badge/Git-grey?logo=git&logoColor=F05032)](https://git-scm.com)                        | Version control for tracking code changes and managing development history.                                                     |
| [![badge](https://img.shields.io/badge/GitHub-grey?logo=github&logoColor=181717)](https://github.com)                   | Secure remote repository for source code storage and collaboration.                                                             |
| [![badge](https://img.shields.io/badge/VSCode-grey?logo=htmx&logoColor=007ACC)](https://code.visualstudio.com)          | Integrated Development Environment (IDE) used for writing, testing, and debugging code.                                         |
| [![badge](https://img.shields.io/badge/Python-grey?logo=python)](https://www.python.org/)                               | Primary backend programming language used to implement application logic, data models, and server-side functionality.           |
| [![badge](https://img.shields.io/badge/Django-grey.svg?logo=django&logoColor=0C4B33)](https://www.djangoproject.com/)   | Backend web framework used to manage authentication, database interactions via ORM, URL routing, and server-rendered templates. |
| [![badge](https://img.shields.io/badge/HTML-grey?logo=html5&logoColor=E34F26)](https://en.wikipedia.org/wiki/HTML)      | Markup language used to structure and present content rendered by Django templates.                                             |
| [![badge](https://img.shields.io/badge/CSS-grey?logo=CSS&logoColor=1572B6)](https://en.wikipedia.org/wiki/CSS)          | Styling language used to control layout, responsiveness, and visual presentation.                                               |
| ![Static Badge](https://img.shields.io/badge/JavaScript-grey?logo=javascript&logoColor=f7df1e)                          | Client-side scripting used to enhance interactivity and user experience.                                                        |
| [![badge](https://img.shields.io/badge/GitHub_Pages-grey?logo=githubpages&logoColor=222222)](https://pages.github.com)  | Hosting platform for the deployed front-end documentation and static assets.                                                    |
| [![badge](https://img.shields.io/badge/Bootstrap-grey?logo=bootstrap&logoColor=7952B3)](https://getbootstrap.com)       | Front-end framework used to implement responsive layouts and reusable UI components.                                            |
| [![badge](https://img.shields.io/badge/Figma-grey?logo=figma&logoColor=F24E1E)](https://www.figma.com)                  | Design tool used to create wireframes and plan UI layout before development.                                                    |
| [![badge](https://img.shields.io/badge/Font_Awesome-grey?logo=fontawesome&logoColor=528DD7)](https://fontawesome.com)   | Icon library used to improve visual clarity and user interface consistency.                                                     |

## Agile Development Process

> StudyStack was developed using Agile methodologies, leveraging GitHub’s project management tools for iterative planning, task tracking, and prioritisation. This ensured the project remained user-focused, adaptable, and transparent throughout its lifecycle.

### GitHub Projects

[GitHub Projects](https://github.com/users/yenmangu/projects/11) served as an Agile tool for this project. Through it, User Stories, issues/bugs, and Milestone tasks were planned, then subsequently tracked on a regular basis using the Kanban project board.

![screenshot](documentation/agile/gh-projects.png)

### GitHub Pages

The site was deployed to GitHub Pages. The steps to deploy are as follows:

- In the [GitHub repository](https://github.com/yenmangu/ci-ms-3-studystack), navigate to the "Settings" tab.
- In Settings, click on the "Pages" link from the menu on the left.
- From the "Build and deployment" section, click the drop-down called "Branch", and select the **main** branch, then click "Save".
- The page will be automatically refreshed with a detailed message display to indicate the successful deployment.
- Allow up to 5 minutes for the site to fully deploy.

The live link can be found on [GitHub Pages](https://yenmangu.github.io/ci-ms-3-studystack/).

### GitHub Issues

GitHub Issues were used to document, discuss, and resolve individual tasks, bugs, and feature ideas.

- **User Stories:** Each key feature began as a user story, often linked to the MoSCoW prioritisation process below.
- **Bugs/Tasks:** Each bug or technical task received its own issue, linked to the appropriate project board column for tracking and resolution.
- **Transparency:** Issue numbers and references appear in commit messages for traceability and auditability.

### MoSCoW Prioritisation

MoSCoW (Must, Should, Could, Won’t Have) was used throughout the project to prioritise user stories and features.
For a full explanation and breakdown, see [MoSCoW Prioritisation](#moscow-prioritisation) under User Stories and Features.

> [!NOTE]
> See [Complex Search](COMPLEX_SEARCH.md) for MoSCoW prioritisation of the full [complexSearch](https://spoonacular.com/food-api/docs#Search-Recipes-Complex) endpoint

## Development Bugs

| Bug/Issue | Diagnosis | Fix | Commit Ref |
| --------- | --------- | --- | ---------- |

## Testing

> [!NOTE]
> For all testing please refer to the [TESTING.md](TESTING.md) file.

## Deployment

### GitHub Pages

### Local Development

> [!IMPORTANT]
> While all of the code is open source, the Node.js API proxy enforces CORS with an allowed origin list for security.
>
> - If you wish to use the official Node.js proxy, please contact the author to request your origin be added.
> - Alternatively, you are welcome to fork this repo and deploy your own proxy.
> - To connect directly to Spoonacular, you’ll need your own (free) API key:
>   [Spoonacular API Portal](https://spoonacular.com/food-api/)

**Note:**
By default, the StudyStack front-end app expects the proxy to be available at the configured API base URL.
You can override this in your environment if running your own version.

#### Cloning

<!-- TODO: Add cloning and forking -->

> Add cloning and forking information

#### Forking

### Local VS Deployment

## Browser Compatibility

## Accessibility

StudyStack was designed and developed with accessibility as a core requirement, not an afterthought.
All visual, navigational, and interactive elements follow recognised accessibility and UX best practices to ensure that the application can be used effectively by users of all abilities and across a range of devices.

A detailed explanation of the accessibility standards followed, design decisions made, and testing performed can be found in the [Accessibility Breakdown](#accessibility-breakdown) section below.

### Approach

The app adheres to [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) principles, prioritising clarity, contrast, and consistent interaction patterns.
Keyboard navigation, ARIA labelling, and semantic HTML were implemented across all pages to support screen readers and alternative input devices.
Focus states are always visible, and users can operate all controls — including toggles and navigation — without a mouse.

### Testing

Accessibility was evaluated throughout development using:

- **Manual keyboard testing** to confirm tab order and logical navigation flow.
- **Automated audits** via Lighthouse and WAVE to detect colour-contrast or ARIA issues.
- **HTML / CSS validation** using W3C validators to maintain semantic integrity.

### Outcome

The result is a mobile-first web application that meets modern accessibility expectations:

- Fully navigable and operable by keyboard alone
- Screen-reader friendly through meaningful structure and ARIA support
- Clear focus indicators and responsive, legible typography
- Accessible colour contrast and error feedback messaging

StudyStack’s accessibility implementation satisfies the Code Institute Level 5 requirements for an interactive front-end project and demonstrates professional, user-centred design practice.

## Credits

### Credits For Specific Features

| Feature | Source | Notes |
| ------- | ------ | ----- |

### Other Credits

| Material                                 | Source                                                   |
| ---------------------------------------- | -------------------------------------------------------- |
| CSS - Block, Element, Modifider Strategy | [BEM-101 on CSS-Tricks](https://css-tricks.com/bem-101/) |
|                                          |                                                          |

### Content

### Media

#### Food/Stock Images & Icons

| Media | Attribution |
| ----- | ----------- |

### Acknowledgements

- I would like to thank my Code Institute mentor, [Tim Nelson](https://www.github.com/TravelTimN) for the support throughout the development of this project.
- I would like to thank the [Code Institute](https://codeinstitute.net) Tutor Team for their assistance with troubleshooting and debugging some project issues.
- I would like to thank the [Code Institute Discord community](https://discord.com/channels/1371431903663489024/1371431904624119901) for the moral support; it kept me going during periods of self doubt and impostor syndrome.
- I would like to thank my employer, for supporting me in my career development change towards becoming a software developer.

---

## Accessibility Breakdown

StudyStack follows a user-centred, inclusive design philosophy in line with
[WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) standards and the Code Institute Level 5 specification for _Interactive Front-End Development_.

Accessibility considerations were applied throughout the design and development process, covering layout, navigation, interaction, and content presentation.

### Design & Layout

- Colour palette verified for WCAG AA contrast compliance.
- Mobile-first responsive layout ensures all users can navigate effectively on any device.
- Legible typography and clear information hierarchy improve readability and comprehension.

### Navigation & Controls

- Every navigation link, toggle, and button is fully keyboard accessible.
- Logical tab order and persistent focus indicators support users with motor or visual impairments.
- All icons and controls include descriptive `aria-label` or `aria-expanded` attributes.

### Media & Feedback

- Images include meaningful `alt` text; decorative elements use empty alt attributes or `aria-hidden="true"`.
- Live content updates use ARIA live regions to announce changes to screen-reader users.
- Error states and progress indicators provide clear, plain-language feedback.

### Validation & Testing

Accessibility was verified through:

- **Manual keyboard testing** and **screen-reader checks**.
- **Automated audits** using Lighthouse, WAVE, and axe DevTools.
- **HTML / CSS validation** with W3C tools to maintain semantic accuracy.

### Reference

Based on _WCAG 2.1 AA_ guidelines and Code Institute Unit 2: Interactive Front End Development,
Criterion 1.1 — “Design a web application that meets accessibility guidelines, follows UX principles, and presents a structured layout and navigation model.”

---

**Result:**
StudyStack delivers a consistent, accessible, and intuitive experience that upholds professional web-accessibility standards across all devices and interaction modes.
