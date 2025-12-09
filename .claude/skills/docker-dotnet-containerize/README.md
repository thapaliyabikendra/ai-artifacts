# .NET Docker Containerization Skill - Usage Guide

## Installation

### Project-Level (Recommended for Teams)
```bash
# Create skills directory in your project
mkdir -p .claude/skills/docker-dotnet-containerize

# Save the skill file
# Copy docker-dotnet-containerize.md to .claude/skills/docker-dotnet-containerize/SKILL.md

# Commit to version control
git add .claude/skills/
git commit -m "Add Docker containerization skill"
git push
```

### Personal-Level (For Individual Use)
```bash
# Create personal skills directory
mkdir -p ~/.claude/skills/docker-dotnet-containerize

# Save the skill file
# Copy docker-dotnet-containerize.md to ~/.claude/skills/docker-dotnet-containerize/SKILL.md
```

## Quick Start

Once installed, the skill activates automatically when you mention Docker or containerization in your .NET project context.

### Basic Usage

**Option 1: Natural Language (Recommended)**
```
You: "I need to containerize my .NET API project"
```

**Option 2: Direct Request**
```
You: "Create Docker setup for this project"
```

**Option 3: Specific Requirements**
```
You: "Generate a Dockerfile for my .NET 8 Clean Architecture solution"
```

### What You'll Get

The skill will automatically:
1. ✅ Analyze your solution structure
2. ✅ Generate optimized Dockerfile
3. ✅ Create .dockerignore file
4. ✅ Provide build commands
5. ✅ Include validation checklist

## Usage Examples

### Example 1: Simple Web API

**You say:**
```
Containerize my ASP.NET Core Web API
```

**Claude will:**
- Detect your project structure
- Generate a simple multi-stage Dockerfile
- Create .dockerignore
- Provide build and run commands

**Expected output files:**
```
your-project/
├── Dockerfile          # Multi-stage build
├── .dockerignore       # Optimized ignore patterns
└── (build commands provided in chat)
```

### Example 2: Clean Architecture Solution

**You say:**
```
I have a Clean Architecture solution with Domain, Application, Infrastructure, and WebApi projects. Set up Docker for it.
```

**Claude will:**
- Map your dependency graph
- Layer COPY commands by dependency order
- Optimize for layer caching
- Generate architecture-aware Dockerfile

### Example 3: Complex Multi-Project DDD Solution

**You say:**
```
Create Docker configuration for my DDD solution:
- 2 Domain projects
- 3 Infrastructure projects  
- 4 Application services
- 1 API gateway
```

**Claude will:**
- Analyze all 10 projects
- Order dependencies correctly
- Create optimized multi-stage build
- Ensure proper layer caching

### Example 4: Specific Optimization Requirements

**You say:**
```
Generate a production-ready Dockerfile for .NET 8 API with:
- Smallest possible image size
- Security best practices
- Health check support
```

**Claude will:**
- Use Alpine Linux images
- Configure non-root user
- Add security optimizations
- Include health check endpoint configuration

## Verification

After the skill runs, verify the generated files:

### Check Dockerfile
```bash
# Validate Dockerfile syntax
docker build --check .

# Build to test
docker build -t test-build .
```

### Check .dockerignore
```bash
# View what will be sent to Docker context
docker build --no-cache --progress=plain . 2>&1 | grep "COPY"
```

### Validate Generated Configuration
Use the checklist Claude provides:
- [ ] .NET version matches your project
- [ ] All projects are included
- [ ] Ports are correctly exposed
- [ ] Non-root user configured
- [ ] Alpine images used

## Testing Your Docker Setup

### Build and Run Locally
```bash
# Build the image
docker build -t myapi:dev .

# Run the container
docker run -d -p 8080:8080 --name myapi-test myapi:dev

# Check if it's running
curl http://localhost:8080/health

# View logs
docker logs -f myapi-test

# Stop and clean up
docker stop myapi-test && docker rm myapi-test
```

### Production Build
```bash
# Build with release configuration
docker build -t myapi:1.0.0 --build-arg BUILD_CONFIGURATION=Release .

# Tag for registry
docker tag myapi:1.0.0 myregistry/myapi:1.0.0

# Push to registry
docker push myregistry/myapi:1.0.0
```

## Common Scenarios

### Scenario 1: Existing Project Without Docker
```
You: "Add Docker support to this existing .NET 6 API"
```
The skill analyzes your current setup and generates appropriate configuration.

### Scenario 2: Upgrading Docker Configuration
```
You: "Update my Dockerfile to use .NET 8 and Alpine Linux"
```
The skill generates a new optimized version.

### Scenario 3: Multi-Container Setup
```
You: "I need Docker setup for my API and background worker service"
```
The skill can handle multiple entry points.

### Scenario 4: Debugging Build Issues
```
You: "My Dockerfile build is failing with 'project not found' error"
```
The skill provides troubleshooting guidance and fixes.

## Tips for Best Results

### 1. Provide Context
**Good:**
```
"Containerize my .NET 8 Clean Architecture solution with separate Domain, Infrastructure, Application, and WebApi projects"
```

**Less Effective:**
```
"Add Docker"
```

### 2. Mention Constraints
```
"Create Dockerfile optimized for small image size and fast rebuilds"
```

### 3. Specify Architecture
```
"I'm using ABP Framework, please generate appropriate Docker setup"
```

### 4. Include Requirements
```
"Need Docker setup with health checks and support for environment variables"
```

## Integration with Development Workflow

### With Version Control
```bash
# After skill generates files
git add Dockerfile .dockerignore
git commit -m "Add Docker containerization"
```

### With CI/CD
The generated Dockerfile works with standard CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Build Docker image
  run: docker build -t ${{ env.IMAGE_NAME }}:${{ github.sha }} .
```

### With Docker Compose
If you need docker-compose later:
```
You: "Can you also create a docker-compose.yml for local development?"
```

## Troubleshooting

### Skill Not Activating

**Problem:** You asked about Docker but the skill didn't activate.

**Solutions:**
1. Verify skill installation:
   ```bash
   # Check if skill file exists
   ls .claude/skills/docker-dotnet-containerize/SKILL.md
   # or
   ls ~/.claude/skills/docker-dotnet-containerize/SKILL.md
   ```

2. Check YAML frontmatter syntax:
   ```bash
   head -n 5 .claude/skills/docker-dotnet-containerize/SKILL.md
   ```

3. Use explicit keywords:
   ```
   "Containerize" or "Docker setup" or "Create Dockerfile"
   ```

### Generated Dockerfile Doesn't Work

**Problem:** Build fails with errors.

**Solutions:**
1. Share the error with Claude:
   ```
   You: "The Docker build failed with this error: [paste error]"
   ```

2. Claude will analyze and provide fixes.

### Need Customization

**Problem:** Generated files need modifications.

**Solution:** Ask for specific changes:
```
You: "Update the Dockerfile to include curl for health checks"
```

## Advanced Usage

### Custom Build Arguments
```
You: "Add build arguments for version and build number to the Dockerfile"
```

### Multi-Stage Build Optimization
```
You: "Optimize the Dockerfile for faster local development rebuilds"
```

### Security Hardening
```
You: "Enhance the Docker configuration with additional security measures"
```

### Size Optimization
```
You: "Can we reduce the final image size further? Currently at 150MB"
```

## Skill Maintenance

### Updating the Skill

When new best practices emerge:
```bash
# Edit the skill
nano .claude/skills/docker-dotnet-containerize/SKILL.md

# Test with Claude
# Restart Claude Code session to reload
```

### Sharing with Team

```bash
# Project skill is automatically shared via git
git pull  # Team members get the skill
```

## Getting Help

### Within Claude Code
```
You: "Explain the generated Dockerfile line by line"
You: "Why did you structure the COPY commands this way?"
You: "How can I optimize this further?"
```

### Common Questions

**Q: Can I modify the generated Dockerfile?**  
A: Yes! The generated files are templates. Customize as needed.

**Q: Will this work with my CI/CD pipeline?**  
A: Yes, the Dockerfiles use standard Docker syntax compatible with all platforms.

**Q: How do I handle secrets in the build?**  
A: Use Docker secrets or build arguments. Ask Claude: "How do I handle database connection strings in the Docker build?"

**Q: Can this handle multiple services?**  
A: Yes. Ask: "Create Dockerfiles for both my API and Worker services"

## Performance Tips

### Faster Builds
- Skill already optimizes layer caching
- Keep .dockerignore up to date
- Use Docker BuildKit (enabled by default in modern Docker)

### Smaller Images
- Skill uses Alpine by default
- Ask about trimming: "Can we enable PublishTrimmed?"
- Consider multi-arch builds for production

## Examples of Typical Workflows

### Workflow 1: New Project Setup
```
1. You: "Set up Docker for this new .NET 8 API project"
2. Claude: [Generates Dockerfile and .dockerignore]
3. You: "Test it"
   docker build -t myapi:test .
4. You: "Works great! Can you add a health check?"
5. Claude: [Updates Dockerfile with HEALTHCHECK]
```

### Workflow 2: Migration from .NET 6 to .NET 8
```
1. You: "Update my Dockerfile from .NET 6 to .NET 8"
2. Claude: [Generates updated configuration]
3. You: "Also optimize for smaller image size"
4. Claude: [Adds size optimizations]
```

### Workflow 3: Troubleshooting
```
1. You: "My Docker build is failing: [error]"
2. Claude: [Analyzes error and provides fix]
3. You: "Still not working, here's the full output: [logs]"
4. Claude: [Provides detailed solution]
```

## Best Practices

1. **Always commit generated files to version control**
2. **Test locally before pushing**
3. **Use specific tags, not `latest` in production**
4. **Review the validation checklist**
5. **Keep .dockerignore updated as project grows**

## Summary

This skill makes Docker containerization for .NET projects effortless:
- ✅ Automatically activates when you need it
- ✅ Analyzes your specific project structure  
- ✅ Generates production-ready configurations
- ✅ Follows Docker best practices
- ✅ Supports all .NET architectures
