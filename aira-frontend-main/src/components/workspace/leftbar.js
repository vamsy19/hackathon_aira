import React, { useState, useEffect } from 'react';
import { FormControl, InputLabel, Select, MenuItem, Box, Button } from '@mui/material';
import { fetchOrganizations, fetchProjects } from '../../services/api/core';
import { getAllSuperNodes } from '../../services/api/layout';

const Leftbar = ({ addSuperNode, selectedOrganization, setSelectedOrganization, selectedProject, setSelectedProject }) => {
    const [organizations, setOrganizations] = useState([]);
    const [projects, setProjects] = useState([]);
    const [superNodes, setSuperNodes] = useState([]);

    useEffect(() => {
        const loadOrganizations = async () => {
            try {
                const orgs = await fetchOrganizations();
                setOrganizations(orgs);
            } catch (error) {
                console.error('Error fetching organizations:', error);
            }
        };

        const loadProjects = async () => {
            try {
                const projs = await fetchProjects();
                setProjects(projs);
            } catch (error) {
                console.error('Error fetching projects:', error);
            }
        };

        const loadSuperNodes = async () => {
            try {
                const nodes = await getAllSuperNodes();
                setSuperNodes(nodes);
            } catch (error) {
                console.error('Error fetching super nodes:', error);
            }
        };

        loadOrganizations();
        loadProjects();
        loadSuperNodes();
    }, []);

    const handleOrganizationChange = (event) => {
        setSelectedOrganization(event.target.value);
    };

    const handleProjectChange = (event) => {
        setSelectedProject(event.target.value);
    };

    return (
        <Box sx={{ padding: 2 }}>
            <FormControl fullWidth sx={{ marginBottom: 2 }}>
                <InputLabel id="organization-label">Organization</InputLabel>
                <Select
                    labelId="organization-label"
                    value={selectedOrganization}
                    onChange={handleOrganizationChange}
                >
                    {organizations.map((org) => (
                        <MenuItem key={org.id} value={org.id}>
                            {org.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <FormControl fullWidth>
                <InputLabel id="project-label">Project</InputLabel>
                <Select
                    labelId="project-label"
                    value={selectedProject}
                    onChange={handleProjectChange}
                >
                    {projects.map((proj) => (
                        <MenuItem key={proj.id} value={proj.id}>
                            {proj.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <Box sx={{ marginTop: 2 }}>
                {superNodes.map((node) => (
                    <Button onClick={()=>addSuperNode(node)} key={node.id} variant="contained" sx={{ marginBottom: 1 }}>
                        {node.name}
                    </Button>
                ))}
            </Box>
        </Box>
    );
};

export default Leftbar;